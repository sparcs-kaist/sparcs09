/*
 * Hack: Temporal plugin for client init (will be removed after nuxt 1.0 released)
 */
export default async (ctx) => {
  await ctx.store.dispatch('nuxtClientInit', ctx);
};
