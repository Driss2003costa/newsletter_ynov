import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { SendRecord, Settings } from '../types'

interface State {
  settings: Settings
  history: SendRecord[]
  setSettings: (patch: Partial<Settings>) => void
  addRecord: (record: SendRecord) => void
  clearHistory: () => void
}

const defaultSettings: Settings = {
  fromName: 'Newsletter Ynov',
  fromEmail: 'onboarding@resend.dev',
  replyTo: '',
}

export const useStore = create<State>()(
  persist(
    (set) => ({
      settings: defaultSettings,
      history: [],
      setSettings: (patch) => set((s) => ({ settings: { ...s.settings, ...patch } })),
      addRecord: (record) => set((s) => ({ history: [record, ...s.history].slice(0, 100) })),
      clearHistory: () => set({ history: [] }),
    }),
    { name: 'newsletter_ynov' },
  ),
)
