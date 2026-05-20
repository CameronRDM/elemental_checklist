use rocket::{get, post, serde::json::Json, State};
use sqlx::PgPool;
use uuid::Uuid;
use crate::models::{Set, Card, Collection, AddCardRequest};

pub struct FirebaseUser(pub String);

#[rocket::async_trait]
impl<'r> rocket::request::FromRequest<'r> for FirebaseUser {
    type Error = ();

    async fn from_request(request: &'r rocket::request::Request<'_>) -> rocket::request::Outcome<Self, Self::Error> {
        let auth_header = request.headers().get_one("Authorization");
        match auth_header {
            Some(token) if token.starts_with("Bearer ") => {
                let uid = token.trim_start_matches("Bearer ").to_string();
                rocket::request::Outcome::Success(FirebaseUser(uid))
            }
            _ => rocket::request::Outcome::Forward(rocket::http::Status::Unauthorized),
        }
    }
}

#[get("/sets")]
pub async fn get_sets(pool: &State<PgPool>) -> Result<Json<Vec<Set>>, rocket::http::Status> {
    let sets = sqlx::query_as::<_, Set>("SELECT * FROM sets")
        .fetch_all(pool.inner())
        .await
        .map_err(|_| rocket::http::Status::InternalServerError)?;
    Ok(Json(sets))
}

#[get("/sets/<set_id>/cards")]
pub async fn get_cards(pool: &State<PgPool>, set_id: Uuid) -> Result<Json<Vec<Card>>, rocket::http::Status> {
    let cards = sqlx::query_as::<_, Card>("SELECT * FROM cards WHERE set_id = $1 ORDER BY number")
        .bind(set_id)
        .fetch_all(pool.inner())
        .await
        .map_err(|_| rocket::http::Status::InternalServerError)?;
    Ok(Json(cards))
}

#[get("/collection")]
pub async fn get_collection(pool: &State<PgPool>, user: FirebaseUser) -> Result<Json<Vec<Collection>>, rocket::http::Status> {
    let collection = sqlx::query_as::<_, Collection>("SELECT * FROM collection WHERE firebase_uid = $1")
        .bind(&user.0)
        .fetch_all(pool.inner())
        .await
        .map_err(|_| rocket::http::Status::InternalServerError)?;
    Ok(Json(collection))
}

#[post("/collection/add", data = "<req>")]
pub async fn add_to_collection(pool: &State<PgPool>, user: FirebaseUser, req: Json<AddCardRequest>) -> Result<Json<Collection>, rocket::http::Status> {
    let mut tx = pool.begin().await.map_err(|_| rocket::http::Status::InternalServerError)?;

    let existing = sqlx::query_as::<_, Collection>(
        "SELECT * FROM collection WHERE firebase_uid = $1 AND card_id = $2 AND variant = $3"
    )
    .bind(&user.0)
    .bind(req.card_id)
    .bind(&req.variant)
    .fetch_optional(&mut *tx)
    .await
    .map_err(|_| rocket::http::Status::InternalServerError)?;

    let record = match existing {
        Some(mut coll) => {
            coll.quantity += 1;
            sqlx::query_as::<_, Collection>(
                "UPDATE collection SET quantity = $1 WHERE id = $2 RETURNING *"
            )
            .bind(coll.quantity)
            .bind(coll.id)
            .fetch_one(&mut *tx)
            .await
            .map_err(|_| rocket::http::Status::InternalServerError)?
        }
        None => {
            sqlx::query_as::<_, Collection>(
                "INSERT INTO collection (id, firebase_uid, card_id, variant, quantity, acquired_at) VALUES ($1, $2, $3, $4, $5, NOW()) RETURNING *"
            )
            .bind(Uuid::new_v4())
            .bind(&user.0)
            .bind(req.card_id)
            .bind(&req.variant)
            .bind(1)
            .fetch_one(&mut *tx)
            .await
            .map_err(|_| rocket::http::Status::InternalServerError)?
        }
    };

    tx.commit().await.map_err(|_| rocket::http::Status::InternalServerError)?;

    Ok(Json(record))
}
