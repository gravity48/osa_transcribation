

export default function (ctx) {
  ctx.$axios.onError((error) => {
    if (error.response.status === 401) {
      ctx.$auth.logout();
      ctx.redirect('/login');
    }
  })
}
