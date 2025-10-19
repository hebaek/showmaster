import { smlib } from './smlib/smlib.js'



$(document).ready(async () => {
    const value = await smlib.storage.load_local('key')
    console.log(value)
})
