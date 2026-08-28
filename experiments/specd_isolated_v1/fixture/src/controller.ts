import { serviceValue } from './service'

export function controllerValue(input: number): number {
  return serviceValue(input) + 3
}
