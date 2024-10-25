async function isAuth() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

  const user = await db?.auth?.getUser();

  if (user?.data?.user) {
    return true;
  } else {
    return false;
  }
}

async function getUser() {
  /** @type {import("../../types").DBClient} */
  const db = /** @type {*} */ (window).db;

  const user = (await db.auth.getUser()).data.user;
  return user;
}
