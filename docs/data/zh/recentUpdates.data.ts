import { createRecentUpdatesLoader } from '@nolebase/vitepress-plugin-index/vitepress'

export default createRecentUpdatesLoader({
  dir: 'zh',
  rewrites: [
    { from: /^pages\/zh\//, to: '' },
  ],
  ignores: [
    '**/snippets/**.md',
  ],
})
