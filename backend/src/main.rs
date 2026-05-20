#[macro_use] extern crate rocket;

mod models;
mod db;
mod routes;

use rocket_cors::{AllowedHeaders, AllowedOrigins, CorsOptions};

#[launch]
async fn rocket() -> _ {
    dotenvy::dotenv().ok();
    
    let pool = db::init_pool().await.expect("Failed to initialize database pool");

    let cors = CorsOptions::default()
        .allowed_origins(AllowedOrigins::all())
        .allowed_headers(AllowedHeaders::all())
        .allow_credentials(true)
        .to_cors()
        .expect("Error creating CORS fairing");

    rocket::build()
        .manage(pool)
        .attach(cors)
        .mount("/api", routes![
            routes::get_sets,
            routes::get_cards,
            routes::get_collection,
            routes::add_to_collection
        ])
}
