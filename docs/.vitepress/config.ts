import type { DefaultTheme } from 'vitepress'

import { argv, cwd, env } from 'node:process'
import { BiDirectionalLinks } from '@nolebase/markdown-it-bi-directional-links'
import { UnlazyImages } from '@nolebase/markdown-it-unlazy-img'
import { InlineLinkPreviewElementTransform } from '@nolebase/vitepress-plugin-inline-link-preview/markdown-it'
import { transformHeadMeta } from '@nolebase/vitepress-plugin-meta/vitepress'
import { buildEndGenerateOpenGraphImages } from '@nolebase/vitepress-plugin-og-image/vitepress'
import { calculateSidebar } from '@nolebase/vitepress-plugin-sidebar'
import { transformerTwoslash } from '@shikijs/vitepress-twoslash'
import { gray } from 'colorette'
import MarkdownItFootnote from 'markdown-it-footnote'
import { defineConfig } from 'vitepress'
import { MermaidMarkdown, MermaidPlugin } from 'vitepress-plugin-mermaid'

import packageJSON from '../../package.json'
import { compilerOptions } from './twoslashConfig'

function noTwoslash() {
  return argv.some(v => v.includes('vitepress')) && argv.includes('dev')
}

export const sidebars: Record<string, DefaultTheme.SidebarItem[] | DefaultTheme.SidebarMulti> = {
  en: {
    '/en/': calculateSidebar(['en/guide', 'en/integrations', 'en/releases'], undefined, { '/': 4 }),
    '/en/ui/': calculateSidebar(['en/ui'], undefined, { '/': 2 }),
  } as DefaultTheme.SidebarMulti,
  zh: {
    '/zh/': calculateSidebar(['zh/guide', 'zh/knowledge', 'zh/models', 'zh/integrations'], undefined, { '/': 2 }),
    '/zh/ui/': calculateSidebar(['zh/ui'], undefined, { '/': 2 }),
  } as DefaultTheme.SidebarMulti,
}
function getVueProdHydrationMismatchDetailsFlag() {
  if (!env) {
    console.warn('WARNING: env is not available when trying to get Vue Prod Hydration Mismatch Details Flag')
    throw new Error('env is not available')
  }

  return !!env.VUE_PROD_HYDRATION_MISMATCH_DETAILS_FLAG
}

// https://vitepress.dev/reference/site-config
export default defineConfig({
  vite: {
    define: {
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: getVueProdHydrationMismatchDetailsFlag(),
    },
    plugins: [MermaidPlugin()], // add plugins
    optimizeDeps: { // include mermaid
      include: ['mermaid'],
    },
    ssr: {
      noExternal: ['mermaid'],
    },
  },
  vue: {
    template: {
      transformAssetUrls: {
        video: ['src', 'poster'],
        source: ['src'],
        img: ['src'],
        image: ['xlink:href', 'href'],
        use: ['xlink:href', 'href'],
        NolebaseUnlazyImg: ['src'],
      },
    },
  },
  cleanUrls: true,
  ignoreDeadLinks: [
    // Site Config | VitePress
    // https://vitepress.dev/reference/site-config#ignoredeadlinks
    //
    // ignore all localhost links
    /^https?:\/\/localhost/,
  ],
  head: [
    // Proxying Plausible through Netlify | Plausible docs
    // https://plausible.io/docs/proxy/guides/netlify
    ['script', { 'defer': 'true', 'data-domain': '', 'data-api': '', 'src': '' }],
    ['link', { rel: 'icon', href: '/DMXAPI.png' }],
  ],
  themeConfig: {
    // Only enable this on debug component style
    // externalLinkIcon: true,
    outline: 'deep',
    socialLinks: [
      { icon: 'devpost', link: 'https://dmxapi.cn/' },
      { icon: 'github', link: 'https://github.com/dmxapi' },
      { icon: 'x', link: 'https://dmxapi.cn/' },
      { icon: 'wechat', link: 'https://dmxapi.cn/models.html#contact' },
    ],
    footer: {
      copyright: 'Copyright © 2023 - 2025 DMXAPI, LLC',
    },
    search: {
      provider: 'local',
      options: {
        locales: {
          zh: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档',
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                },
              },
            },
          },
        },
      },
    },
  },
  buildConcurrency: 1000,
  locales: {
    en: {
      label: 'English',
      lang: 'en',
      link: '/en/',
      title: 'DMXAPI',
      description: 'A collection of diverse documentation engineering tools',
      themeConfig: {
        nav: [
          {
            text: 'Guide',
            items: [
              { text: 'Getting Started', link: '/en/guide/getting-started' },
              { text: 'Recent Updated', link: '/en/recent-updates' },
            ],
          },
          { text: 'Integrations', link: '/en/integrations/' },
          { text: 'UI Components', link: '/en/ui/' },
          {
            text: packageJSON.version,
            items: [
              {
                text: 'Migrations',
                items: [
                  {
                    text: 'Migrate from v1 to v2',
                    link: '/en/releases/migrations/v1-to-v2',
                  },
                  {
                    text: 'Migrate from v2 to v3',
                    link: '/en/releases/migrations/v2-to-v3',
                  },
                ],
              },
            ],
          },
        ],
        sidebar: sidebars.en,
      },
    },
    root: {
      label: '简体中文',
      lang: 'zh',
      link: '/zh/',
      title: 'DMXAPI 文档',
      description: '一个 Key 使用全球大模型',
      themeConfig: {
        nav: [
          {
            text: '快速入门',
            items: [
              { text: '快速开始', link: '/zh/guide/getting-started' },
              { text: '最近更新', link: '/zh/guide/recent-updates' },
            ],
          },
          { text: '上新日志', link: '/zh/integrations/' },
          { text: '接入教程', link: '/zh/ui/' },
          {
            text: '模型列表',
            items: [
              {
                text: 'OpenAI 系列',
                items: [
                  {
                    text: 'GPT-4',
                    link: '/zh/releases/migrations/v1-to-v2',
                  },
                  {
                    text: 'GPT-4o',
                    link: '/zh/releases/migrations/v2-to-v3',
                  },
                ],
              },
              {
                text: 'Gemini 系列',
                items: [
                  {
                    text: 'Gemini 1.5 Pro',
                    link: '/zh/releases/migrations/v1-to-v2',
                  },
                  {
                    text: 'Gemini 1.5 Flash',
                    link: '/zh/releases/migrations/v2-to-v3',
                  },
                ],
              },
              {
                text: 'DeepSeek 系列',
                items: [
                  {
                    text: 'DeepSeek Coder',
                    link: '/zh/releases/migrations/v1-to-v2',
                  },
                  {
                    text: 'DeepSeek Coder Plus',
                    link: '/zh/releases/migrations/v2-to-v3',
                  },
                ],
              },
            ],
          },
        ],
        sidebar: sidebars.zh,
      },
    },
  },
  rewrites: {
    '/': '/index.md',
  },
  markdown: {
    codeTransformers: noTwoslash()
      ? []
      : [
          transformerTwoslash({
            errorRendering: 'hover',
            onTwoslashError(error, _, __, ___) {
              console.error('Twoslash Error:', (error as Error)?.message, '\n', (error as Error)?.stack ? gray(String((error as Error)?.stack)) : '')
            },
            twoslashOptions: compilerOptions,
          }),
        ],
    preConfig(md) {
      md.use(BiDirectionalLinks({
        dir: cwd(),
      }))
      md.use(UnlazyImages(), {
        imgElementTag: 'NolebaseUnlazyImg',
      })
    },
    config(md) {
      md.use(MarkdownItFootnote)
      md.use(InlineLinkPreviewElementTransform)
      md.use(MermaidMarkdown)
    },
  },
  async transformHead(context) {
    let head = [...context.head]

    const returnedHead = await transformHeadMeta()(head, context)
    if (typeof returnedHead !== 'undefined')
      head = returnedHead

    return head
  },
  async buildEnd(siteConfig) {
    const newBuilder = buildEndGenerateOpenGraphImages({
      baseUrl: 'https://nolebase-integrations.ayaka.io',
      category: {
        byPathPrefix: [
          { prefix: '/en/integrations/markdown-it-bi-directional-links', text: 'Markdown It Plugins: Bi-directional links' },
          { prefix: '/en/integrations/markdown-it', text: 'Markdown It Plugins' },
          { prefix: '/en/integrations/obsidian-plugin', text: 'Obsidian Plugins' },
          { prefix: '/en/integrations/vitepress-plugin-inline-link-preview', text: 'VitePress Plugin: Inline Links Previewing' },
          { prefix: '/en/integrations/vitepress-plugin-git-changelog', text: 'VitePress Plugin: Git-based page histories' },
          { prefix: '/en/integrations/vitepress-plugin-thumbnail-hash', text: 'VitePress Plugin: Thumbnail hashing for images' },
          { prefix: '/en/integrations/vitepress-plugin', text: 'VitePress Plugins' },
          { prefix: '/en/integrations/', text: 'Integrations' },
          { prefix: '/en/guide/', text: 'Guide' },
          { prefix: '/en/ui/', text: 'UI Components' },
          { prefix: '/en/', text: 'Documentations' },
          { prefix: '/zh/integrations/markdown-it-bi-directional-links', text: 'Markdown It 插件：双向链接' },
          { prefix: '/zh/integrations/markdown-it', text: 'Markdown It 插件' },
          { prefix: '/zh/integrations/obsidian-plugin', text: 'Obsidian 插件' },
          { prefix: '/zh/integrations/vitepress-plugin-inline-link-preview', text: 'VitePress 插件：行内链接预览' },
          { prefix: '/zh/integrations/vitepress-plugin-git-changelog', text: 'VitePress 插件：变更日志 及 文件历史' },
          { prefix: '/zh/integrations/vitepress-plugin-thumbnail-hash', text: 'VitePress 插件：缩略图模糊哈希生成' },
          { prefix: '/zh/integrations/vitepress-plugin', text: 'VitePress 插件' },
          { prefix: '/zh/integrations/', text: '集成' },
          { prefix: '/zh/guide/', text: '指南' },
          { prefix: '/zh/ui/', text: 'UI 组件' },
          { prefix: '/zh/', text: '文档' },
        ],
        fallbackWithFrontmatter: true,
      },
    })

    await newBuilder(siteConfig)
  },
})
