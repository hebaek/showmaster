const modules = {
    toolbar: { enable: true, file: '../plugins/toolbar.js' },
    manus:   { enable: true, file: '../plugins/manus.js'   },
    pdf:     { enable: true, file: '../plugins/pdf.js'     },
}



const features = {
    manus: {
        load: true,
        save: true,
        edit: true,
    },
    cues: {
        load: true,
        save: true,
        edit: true,
    },
}



export const flags = {
    modules:  modules,
    features: features,
}
