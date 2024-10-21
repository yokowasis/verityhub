async function isAuth() {
  /** @type {import("@supabase/supabase-js").SupabaseClient} */
  const db = /** @type {*} */ (window).db;

  const user = await db?.auth?.getUser();

  if (user.data?.user) {
    return true;
  } else {
    return false;
  }
}

isAuth().then((s) => {
  console.log(s);
});
