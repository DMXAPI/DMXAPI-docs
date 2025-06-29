import type { Plugin } from 'vue'

import { NuLazyTeleportRiveCanvas } from '@nolebase/ui-rive-canvas'
import { defineThemeUnconfig } from '@nolebase/unconfig-vitepress'

import { NolebasePluginPreset } from '@nolebase/unconfig-vitepress/plugins'
import TwoslashFloatingVue from '@shikijs/vitepress-twoslash/client'
import { MotionPlugin } from '@vueuse/motion'
import { h } from 'vue'
import AIModelsList from './components/AIModelsList.vue'
import DifyChatbot from './components/DifyChatbot.vue'
import Footer from './components/Footer.vue'
import HomeContent from './components/HomeContent.vue'
import IntegrationCard from './components/IntegrationCard.vue'
import IntroductionLIBlock from './components/IntroductionLIBlock.vue'
import IntroductionRIBlock from './components/IntroductionRIBlock.vue'
import NavHeader from './components/NavHeader.vue'
import ThumbhashPreview from './components/ThumbhashPreview.vue'
import TrustList from './components/TrustList.vue'
import VPHeroImageLogo from './components/VPHeroImageLogo.vue'
import 'virtual:uno.css'
import '@shikijs/vitepress-twoslash/style.css'
import 'asciinema-player/dist/bundle/asciinema-player.css'
import './styles/vars.css'
import './styles/main.css'

export default defineThemeUnconfig({
  layout: {
    slots: {
      'layout-top': {
        node: [
          () => h(NuLazyTeleportRiveCanvas),
        ],
      },
      'home-hero-before': {
        node: [
          () => h(NavHeader),
        ],
      },
      'home-hero-image': {
        node: [
          () => h(VPHeroImageLogo),
        ],
      },
      'layout-bottom': {
        node: [
          () => h(DifyChatbot),
          () => h(Footer),
        ],
      },
    },
  },
  enhanceApp: ({ app }) => {
    app.component('IntegrationCard', IntegrationCard)
    app.component('HomeContent', HomeContent)
    app.component('ThumbhashPreview', ThumbhashPreview)
    app.component('TrustList', TrustList)
    app.component('IntroductionLIBlock', IntroductionLIBlock)
    app.component('IntroductionRIBlock', IntroductionRIBlock)
    app.component('AIModelsList', AIModelsList)
    app.component('Footer', Footer)
    app.use(TwoslashFloatingVue as Plugin)
    app.use(MotionPlugin as Plugin)
  },
  pluginPresets: [
    NolebasePluginPreset({
      gitChangelog: {
        enable: true,
        options: {
          commitsRelativeTime: true,
        },
      },
    }),
  ],
})
