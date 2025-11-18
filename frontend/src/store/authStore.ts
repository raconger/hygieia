import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  email: string
  fullName: string | null
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User, token: string) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        // TODO: Implement actual login API call
        // For now, mock authentication
        const mockUser = { id: 1, email, fullName: 'Demo User' }
        const mockToken = 'demo_token'
        set({ user: mockUser, token: mockToken, isAuthenticated: true })
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false })
      },

      setUser: (user: User, token: string) => {
        set({ user, token, isAuthenticated: true })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
