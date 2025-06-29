import { smlib } from './smlib.js'



const staticdata = {
    manus: null,
    cues:  null,
}



const resources = data => {
    if (! smlib.test_flags(['data', 'load'])) return

    return new Promise((resolve, reject) => {
        $.ajax({
            url: 'service.php',
            method: 'POST',
            data: data,
            dataType: data.format,
            success: function (response, status, xhr) {
                resolve(response)
            },
            error: function (xhr, status, error) {
                console.error('Error:', error)
                console.error('Status:', status)
                console.error('Response:', xhr.responseText)
                reject(error)
            }
        })
    })
}



const load = async data => {
    data.action = 'load'
    data.format = 'json'

    staticdata[data.content] = await resources(data)
}



const save = data => {
    data.action = 'save'
    data.format = 'json'

    resources(data)
}



const save_cues = async data => {
    save({
        content: 'cues',
        revision: Math.floor(Math.random() * 1000000000),
        json: JSON.stringify(data.cues)
    })
    $('#save_cues, #revert_cues').hide()
}



const revert_cues = async () => {
    await load({ content: 'cues' })
    $('#save_cues, #revert_cues').hide()
}



export const data = {
    load:  load,
    save:  save,

    save_cues:   save_cues,
    revert_cues: revert_cues,

    get manus() { return staticdata.manus },
    get cues()  { return staticdata.cues  },
}
