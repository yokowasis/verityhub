import { serve } from "https://deno.land/std@0.131.0/http/server.ts";
import { Client } from "https://deno.land/x/postgres@v0.17.0/mod.ts";
import { config } from "https://deno.land/x/dotenv@v3.2.2/mod.ts";

const env = config();

console.log(env);

// PostgreSQL connection configuration
const dbConfig = {
  user: env.POSTGRES_USER,
  password: env.POSTGRES_PASSWORD,
  database: env.POSTGRES_DATABASE,
  hostname: env.POSTGRES_HOSTNAME,
  port: env.POSTGRES_PORT,
};

const client = new Client(dbConfig);

// Deno HTTP server handler
async function handler(req: Request): Promise<Response> {
  if (req.method === "GET") {
    // get url params called text
    const { searchParams } = new URL(req.url);
    const text = searchParams.get("text");

    const vec = await (
      await fetch(`https://nlp.backend.b.app.web.id/api/vectorize`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
        }),
      })
    ).json();

    try {
      // Connect to PostgreSQL
      await client.connect();

      // Run the query to select all posts
      const result = (
        await client.queryObject(
          `SELECT * FROM knn_search_posts('[${vec}]'::vector(1024),10)`
        )
      ).rows;

      // Close the connection
      await client.end();

      // Return the result as JSON
      return new Response(JSON.stringify(result), {
        headers: { "Content-Type": "application/json" },
        status: 200,
      });
    } catch (error) {
      console.error("Database error:", error);
      return new Response(JSON.stringify({ error: "Internal Server Error" }), {
        headers: { "Content-Type": "application/json" },
        status: 500,
      });
    }
  } else {
    return new Response("Not Found", { status: 404 });
  }
}

serve(handler, {
  port: 3000,
});
