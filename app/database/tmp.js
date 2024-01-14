connect((conn) => {
  conn.execute();
  conn.commit();
});

function connect(f) {
  conn = open();
  try {
    f(conn);
  } finally {
    conn.close();
  }
}
