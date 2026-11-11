import {defineTheme} from '@astryxdesign/core/theme';
export const kn2pTheme = defineTheme({
  name: 'kn2p',
  color: {accent: '#029ED9', neutralStyle: 'cool', contrast: 'standard'},
  typography: {
    scale: {base: 16, ratio: 1.2},
    body: {family: 'Inter', fallbacks: '"Noto Sans KR", "Noto Sans JP", -apple-system, system-ui, sans-serif'},
    heading: {weight: 'bold', weights: {1: 'bold', 2: 'bold'}},
  },
  radius: {base: 4, multiplier: 1.5},
});
