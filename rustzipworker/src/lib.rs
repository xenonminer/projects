use serde_json::json;
use worker::*;

mod utils;

fn log_request(req: &Request) {
    console_log!(
        "{} - [{}], located at: {:?}, within: {}",
        Date::now().to_string(),
        req.path(),
        req.cf().coordinates().unwrap_or_default(),
        req.cf().region().unwrap_or("unknown region".into())
    );
}

#[event(fetch)]
pub async fn main(req: Request, env: Env, _ctx: worker::Context) -> Result<Response> {
    log_request(&req);

    // Optionally, get more helpful error messages written to the console in the case of a panic.
    utils::set_panic_hook();

    // Optionally, use the Router to handle matching endpoints, use ":name" placeholders, or "*name"
    // catch-alls to match on specific patterns. Alternatively, use `Router::with_data(D)` to
    // provide arbitrary data that will be accessible in each route via the `ctx.data()` method.
    let router = Router::new();

    // Add as many routes as your Worker needs! Each route will get a `Request` for handling HTTP
    // functionality and a `RouteContext` which you can use to  and get route parameters and
    // Environment bindings like KV Stores, Durable Objects, Secrets, and Variables.

    const htmlcode: &str = r#"
    <!DOCTYPE HTML>
    <html>
        <head>
            <title>Auto File Decompressor</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
        </head>
        <body style="text-align: center; background-color:powderblue;">
            <style>
            #fill {
                border-radius: 8px;
                padding: 10px;
                display: inline-block;
                cursor: text;
            }
            </style>
            <h1 style="padding-top: 5%;">Auto File Decompressor</h1>
            <h2>Browse for a file you would like to have decompressed!</h2>
            <form method="post" action="/" enctype="multipart/form-data" style="padding-top: 2%;">
                <label for="myfile">Select a file:</label>
                <input type="file" id="myfile" name="myfile" accept="application/gzip,application/x-bzip2,application/x-lzip,application/x-lzma,application/x-7z-compressed,application/x-rar-compressed,application/x-gtar,application/zip"> 
                <input type="submit" class="submit" value="Upload">
            </form>
            <p style="padding-top: 20px; color: red;"></p>
        </body>
    </html>
    "#; // use const instead of let to make variable global

    router
        .get("/", |_, _| Response::from_html(htmlcode))
        .post_async("/", |mut req, _ctx| async move {
            let form = req.form_data().await?;
            dbg!(&form);
            if let Some(entry) = form.get("myfile") {
                match entry {
                    FormEntry::File(file) => {
                        let filetype = file.type_();
                        return Response::ok(filetype)
                    }
                    FormEntry::Field(_) => return Response::error("Bad Request a", 400),
                }

                //if !(filetype.iter().any(|i| i=="zip") && filetype.iter().any(|i| i=="tar")) {
                //    Response::error("Bad Request", 400)
                //}

            }
            Response::error("Bad Request b", 400)
        })
        .run(req, env).await
}
