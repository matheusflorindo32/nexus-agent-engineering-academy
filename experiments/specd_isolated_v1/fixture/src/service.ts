import { coreValue } from './core'

export function serviceValue(input: number): number {
  return coreValue(input) * 2
}
