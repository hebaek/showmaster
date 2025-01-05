let lastCounterValue = null

let data = null
let showtime = new Date()
let lastpage = null
let miclist  = null

const jsonUrl         = 'data/data.json'
const pdfUrl_original = 'data/manus-original.pdf'
const pdfUrl_mics     = 'data/manus-mics.pdf'

let pdfDoc      = null
let lastpdfpage = null
let viewportWidth = 0
let viewportHeight = 0

let current_scene = null
let current_music = null
let current_page  = { source: null, target: 1, name: null }



const get_page = (type, page) => {
    if (type == 'source') return data.pagemap.find(p => p.source == page)
    if (type == 'target') return data.pagemap.find(p => p.target == page)
    if (type == 'name'  ) return data.pagemap.find(p => p.name   == page)

    return { source: 1, target: 1, name: null }
}



const set_current_page = (type, page) => {
    const realpage = get_page(type, page)

    current_page.source = realpage.source
    current_page.target = realpage.target
    current_page.name   = realpage.name
}


/*
const setShowtime = () => {
    const h = String(showtime.getHours()).padStart(2, '0')
    const m = String(showtime.getMinutes()).padStart(2, '0')
    const s = String(showtime.getSeconds()).padStart(2, '0')
    document.getElementById('showtime').textContent = `${h}:${m}:${s}`
}



const updateClock = () => {
    const now = new Date()
    const countdown = new Date(showtime - now)

    const wh = String(now.getHours()).padStart(2, '0')
    const wm = String(now.getMinutes()).padStart(2, '0')
    const ws = String(now.getSeconds()).padStart(2, '0')
    document.getElementById('walltime').textContent = `${wh}:${wm}:${ws}`

    const ch = String(countdown.getHours()).padStart(2, '0')
    const cm = String(countdown.getMinutes()).padStart(2, '0')
    const cs = String(countdown.getSeconds()).padStart(2, '0')
    document.getElementById('countdown').textContent = `${ch}:${cm}:${cs}`
}
*/


const fetchJsonData = async () => {
    try {
        const response = await fetch(jsonUrl)
        if (!response.ok) {
            throw new Error('Feil ved lasting av JSON-fil')
        }
        data = await response.json()

        lastpage = get_page('target', Math.max(...data.pagemap.map(p => p.target)))
        miclist  = Object.keys(data.micmap[0]['mics'])


//        showtime = new Date(data.showtime)

//        setShowtime()
        createShortcuts()
        createMicList()
        loadPdf(pdfUrl_mics)
        updateLocation('target', current_page.target)
    } catch (error) {
        console.error('Klarte ikke å laste JSON:', error)
    }
}



const createShortcuts = () => {
    data.scenes.forEach((scene) => {
        const button = document.createElement("button")
        button.textContent = `${scene.id} - ${scene.name}`
        button.addEventListener("click", () => {
            updateLocation('target', scene.start.page)
            $('.shortcuts').hide()
        })

        $('.shortcuts.scenes').append(button)
    })

    data.music.forEach((music) => {
        const button = document.createElement("button")
        button.textContent = `${music.id} - ${music.name}`
        button.addEventListener("click", () => {
            updateLocation('target', music.start.page)
            $('.shortcuts').hide()
        })

        $('.shortcuts.music').append(button)
        if (music.type == 'instrumental') {
            $(button).addClass('instrumental')
        }
    })

    data.pagemap.forEach((page) => {
        let text = `Side ${page.source}`
        if (page.name) { text += ` - ${page.name}` }

        const button = document.createElement("button")
        button.textContent = text
        button.addEventListener("click", () => {
            updateLocation('target', page.target)
            $('.shortcuts').hide()
        })

        $('.shortcuts.pages').append(button)
    })

    $('.shortcuts button').addClass('shortcut')

}



const createMicList = () => {
    $('#details').html('')

    for (mic of miclist) {
        $('#details').append(`
            <div class='row' id='mic_${mic}'>
                <div class='mic'>${mic}</div>
                <div class='role'></div>
                <div class='actor'></div>
            </div>
        `)
    }
}



const updateMicList = (scene_index, music_index, page) => {
    const pageList = () => {
        const current_ensembles = {}
        for (ensemble in data.ensemblemap) {
            current = data.ensemblemap[ensemble].filter(ens => ens.location.page + ens.location.y < page + 1).pop()
            current_ensembles[ensemble] = current
        }

        const current_mics = data.micmap.filter(mics => mics.location.page + mics.location.y < page + 1).pop()
        const current_roles = {}
        const current_actors = {}

        for (const [mic, data] of Object.entries(current_mics['mics'])) {
            if (data.role)  { current_roles[data.role  ] = mic }
            if (data.actor) { current_actors[data.actor] = mic }
        }



        for (mic in current_mics['mics']) {
            $(`#mic_${mic} > .role` ).html(current_mics['mics'][mic].role)
            $(`#mic_${mic} > .actor`).html(current_mics['mics'][mic].actor)
        }

        const page_lines = data.lines.filter(line => line.location.page + line.location.y < page + 1 && line.location.page + line.location.y >= page)

        $(`.row`).removeClass('active ensemble')
        for (line of page_lines) {
            for (role of line.roles) {
                $(`#mic_${current_roles[role]}`).addClass('active')
            }
            for (ensemble of line.ensembles) {
                const roles  = current_ensembles[ensemble].roles
                const extras = current_ensembles[ensemble].extras

                for (role  of roles ) { $(`#mic_${current_roles[role]}`  ).addClass('ensemble') }
                for (actor of extras) { $(`#mic_${current_actors[actor]}`).addClass('ensemble') }
            }
        }
    }



    const sceneList = () => {
        $(`.row`).removeClass('passive')

        if (scene_index === null) {
            return
        }

        const current_ensembles = {}
        for (ensemble in data.ensemblemap) {
            current = data.ensemblemap[ensemble].filter(ens => ens.location.page + ens.location.y < page + 1).pop()
            current_ensembles[ensemble] = current
        }

        const current_mics = data.micmap.filter(mics => mics.location.page + mics.location.y < page + 1).pop()
        const current_roles = {}

        for (const [mic, data] of Object.entries(current_mics['mics'])) {
            if (data.role) {
                current_roles[data.role] = mic
            }
        }

        const passive_mics = new Set()

        const firstpage = data.scenes[scene_index].start.page
        const lastpage  = data.scenes[scene_index].end.page

        for (let page = firstpage; page < lastpage; page++) {
            const current_ensembles = {}
            for (ensemble in data.ensemblemap) {
                current = data.ensemblemap[ensemble].filter(ens => ens.location.page + ens.location.y < page + 1).pop()
                current_ensembles[ensemble] = current
            }

            const current_mics = data.micmap.filter(mics => mics.location.page + mics.location.y < page + 1).pop()
            const current_roles = {}

            for (const [mic, data] of Object.entries(current_mics['mics'])) {
                if (data.role) {
                    current_roles[data.role] = mic
                }
            }

            const page_lines = data.lines.filter(line => line.location.page + line.location.y < page + 1 && line.location.page + line.location.y >= page)

            for (line of page_lines) {
                for (role of line.roles) {
                    passive_mics.add(current_roles[role])
                }

                for (ensemble of line.ensembles) {
                    const roles  = current_ensembles[ensemble].roles
                    const extras = current_ensembles[ensemble].extras

                    for (role of roles) {
                        passive_mics.add(current_roles[role])
                    }
                    for (role of extras) {
                        passive_mics.add(current_roles[role])
                    }
                }
            }
        }

        for (mic of passive_mics) {
            $(`#mic_${mic}`).addClass('passive')
        }
    }



    pageList()
    sceneList()
}



const loadPdf = async pdfUrl => {
    const loadingTask = pdfjsLib.getDocument(pdfUrl)

    pdfDoc = await loadingTask.promise
    lastpdfpage = pdfDoc.numPages

    renderPdf(current_page.target)
}

const renderPdf = pageNum => {
    if (! pdfDoc) return

    pdfDoc.getPage(pageNum).then((page) => {
        const canvas = document.getElementById('pdf-canvas')
        const context = canvas.getContext('2d')

        const desiredWidth  = $('#pdf-viewer').innerWidth()
        const desiredHeight = $('#pdf-viewer').innerHeight()

        const testViewport = page.getViewport({ scale: 1, })
        const scaleWidth  = desiredWidth  / testViewport.width
        const scaleHeight = desiredHeight / testViewport.height
        const scale = Math.min(scaleWidth, scaleHeight)

        var viewport = page.getViewport({ scale: scale, })
        canvas.height = viewport.height
        canvas.width = viewport.width

        viewportHeight = viewport.height
        viewportWidth = viewport.width

        var renderContext = {
            canvasContext: context,
            viewport: viewport,
        }
        page.render(renderContext)
    })
}




const updateLocation = (type, pagesource) => {
    pagemap = get_page(type, pagesource)

    if (pagemap.source == current_page.source) return
    if (pagemap.target >  lastpage.target    ) return
    if (pagemap.target <  1                  ) return

    current_page = pagemap

    let scene_index = null
    let music_index = null

    let current_scene = `<div class='header empty'>(ingen scene)</div>`
    let current_music  = `<div class='header empty'>(ingen musikk)</div>`

    for (let i = 0; i < data.scenes.length; i++) {
        if (data.scenes[i].start.page <= current_page.target && data.scenes[i].end.page >= current_page.target) {
            current_scene = `<div class='header'>${data.scenes[i].id} - ${data.scenes[i].name}</div>`
            scene_index = i
        }
    }

    for (let i = 0; i < data.music.length; i++) {
        if (data.music[i].start.page <= current_page.target && data.music[i].end.page >= current_page.target) {
            current_music = `<div class='header'>${data.music[i].id} - ${data.music[i].name}</div>`
            music_index = i
        }
    }

    $('.scenes > .content').html(`${current_scene}`)
    $('.music > .content').html(`${current_music}`)
    $('.pages > .content').html(`<div class='header'>Side ${current_page.source} av ${lastpage.source}</div>`)

    renderPdf(current_page.target)
    updateMicList(scene_index, music_index, current_page.target)
}



const prevScene = () => {
    for (let i = data.scenes.length - 1; i >= 0; i--) {
        if (data.scenes[i].end.page < current_page.target) {
            updateLocation('target', data.scenes[i].start.page)
            return
        }
    }
}



const nextScene = () => {
    for (let i = 0; i < data.scenes.length; i++) {
        if (data.scenes[i].start.page > current_page.target) {
            updateLocation('target', data.scenes[i].start.page)
            return
        }
    }
}



const prevMusic = () => {
    for (let i = data.music.length - 1; i >= 0; i--) {
        if (data.music[i].end.page < current_page.target) {
            updateLocation('target', data.music[i].start.page)
            return
        }
    }
}



const nextMusic = () => {
    for (let i = 0; i < data.music.length; i++) {
        if (data.music[i].start.page > current_page.target) {
            updateLocation('target', data.music[i].start.page)
            return
        }
    }
}



const setHandlers = () => {
    $(window).on('resize', () => renderPdf(current_page.target))

    $(document).on('click', '.scenes > .content', () => { $('.shortcuts:not(.scenes)').hide(); $('.shortcuts.scenes').toggle() })
    $(document).on('click', '.music > .content',  () => { $('.shortcuts:not(.music)' ).hide(); $('.shortcuts.music' ).toggle() })
    $(document).on('click', '.pages > .content',  () => { $('.shortcuts:not(.pages)' ).hide(); $('.shortcuts.pages' ).toggle() })

    $(document).on('click', '.scenes > .prev', () => { prevScene() })
    $(document).on('click', '.scenes > .next', () => { nextScene() })

    $(document).on('click', '.music > .prev', () => { prevMusic() })
    $(document).on('click', '.music > .next', () => { nextMusic() })

    $(document).on('click', '.pages > .prev', () => { updateLocation('target', current_page.target - 1) })
    $(document).on('click', '.pages > .next', () => { updateLocation('target', current_page.target + 1) })

    $(document).on('click', '#pdf-original', () => { loadPdf(pdfUrl_original) })
    $(document).on('click', '#pdf-mics',     () => { loadPdf(pdfUrl_mics) })



//    $(document).on('mousemove', '#pdf-canvas', async event => { c = getPdfCoordinates(event).then(c => { $('.showtime .header').html("y:" + c.y) }) })
}



const getPdfCoordinates = async event => {
    const result = await pdfDoc.getPage(current_page.target).then((page) => {
        const canvas = document.getElementById('pdf-canvas')
        const rect = canvas.getBoundingClientRect()
        const x = event.clientX - rect.left
        const y = event.clientY - rect.top

        relative_x = Math.round(x / viewportWidth  * 1000) / 1000
        relative_y = Math.round(y / viewportHeight * 1000) / 1000

        return { x: relative_x, y: relative_y }
    })

    return result
}



const checkForChanges = async () => {
    try {
        const response = await fetch('updates.php')
        const currentCounter = await response.text()
console.log(currentCounter)

        // Check if the counter value has changed
        if (lastCounterValue !== null && currentCounter !== lastCounterValue) {
            alert('File has changed!') // Trigger your desired action
        }

        // Update the cached counter value
        lastCounterValue = currentCounter;
    } catch (error) {
        console.error('Error checking for changes:', error);
    }
}



$(document).ready(function() {
    fetchJsonData()

//    setInterval(updateClock, 25)
//    updateClock()
//    setShowtime()

    setHandlers()

// Poll the PHP script every 60 seconds (adjust as needed)
//    setInterval(checkForChanges, 60000) // 60,000 ms = 1 minute
//    checkForChanges() // Initial check
})
