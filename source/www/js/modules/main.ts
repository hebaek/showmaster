import { smlib } from './smlib.js'



const init_modules = async (): Promise<void> => {
    const modules = smlib.modules()

    for (const m in modules) {
        const module = modules[m]
        if (!module.enable) continue

        const { setup } = await import(module.file)
        setup()
    }
}



$(document).ready(() => {
    init_modules()
    .catch(error => console.error('Error initializing modules:', error))
})
