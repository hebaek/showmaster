const projectfile = 'data/shows.json'
const projectdata = {}
const pdfdata     = {}

let showdata = null

const state = {
    'firstpage':    null,
    'lastpage':     null,

    'currentpage':  null,
    'currentscene': null,
    'currentmusic': null,

    'doc':          null,
}






const fetch_showdata = async () => {
    try {
        const response = await fetch(projectfile)
        if (!response.ok) { throw new Error('Feil ved lasting av showdata') }

        const shows = await response.json()

        for (const show in shows.showdata) {
            console.log(show, shows.showdata[show])
            projectdata[show] = {
                'url':  shows.showdata[show].url,
                'name': shows.showdata[show].name,
                'date': shows.showdata[show].date,
                'time': shows.showdata[show].time,
            }
        }

        for (const pdf in shows.pdf) {
            pdfdata[pdf] = {
                'url':  shows.pdf[pdf].url,
                'name': shows.pdf[pdf].name,
            }
        }

        state['currentpage'] = 1
    } catch (error) {
        console.error('Klarte ikke å laste JSON:', error)
    }
}






const load_show = async (show) => {
    try {
        const response = await fetch(projectdata[show].url)
        if (!response.ok) { throw new Error('Feil ved lasting av showdata') }

        return await response.json()
    } catch (error) {
        console.error('Klarte ikke å laste JSON:', error)
    }
}






const get_current_show = async () => {
    return 'Show 1'
}






const populate_show = async show => {
    showdata = await load_show(show)

    pdf_load('mics')

    console.log(showdata)
    create_shortcuts(showdata)
    create_miclist(showdata)

    $('#pdf-original').html(projectdata[show].name)
}






const create_shortcuts = () => {
    showdata.scenes.forEach(scene => {
        let classes = 'shortcut'
        let text = `${scene.id} - ${scene.name}`

        $('.shortcuts.scenes').append(`<button class='${classes}' data-page='${scene.start.page.target}'>${text}</button>`)
    })

    showdata.music.forEach(music => {
        let classes = 'shortcut'; if (music.type == 'instrumental') { classes += ' instrumental' }
        let text = `${music.id} - ${music.name}`

        $('.shortcuts.music').append(`<button class='${classes}' data-page='${music.start.page.target}'>${text}</button>`)
    })

    showdata.pagemap.forEach(page => {
        let classes = 'shortcut'
        let text = `Side ${page.source}`; if (page.name) { text += ` - ${page.name}` }

        $('.shortcuts.pages').append(`<button class='${classes}' data-page='${page.target}'>${text}</button>`)
    })
}






const create_miclist = () => {
    $('#miclist').html('')

    for (const mic of showdata.miclist) {
        $('#miclist').append(`
            <div class='row' id='mic_${mic}'>
                <div class='mic'>${mic}</div>
                <div class='role'></div>
                <div class='actor'></div>
            </div>
        `)
    }
}






const update_miclist = () => {
    const micmap = showdata.micmap.filter(row => row.location.target < state['currentpage'] + 0.99).pop()
    const lines = showdata.lines.filter(line => line.location.target < state['currentpage'] + 1 && line.location.target >= state['currentpage'])
    const roles    = new Set(lines.map(line => line.roles   ).reduce((result, roles) => [...result, ...roles], []))
    const ensemble = new Set(lines.map(line => line.ensemble).reduce((result, roles) => [...result, ...roles], []))

    $('.row').removeClass('passive active role ensemble')
    $('.row > .role').html('')
    $('.row > .actor').html('')

    for (const mic in micmap.mics) {
        // Go through all roles on page
        if (roles.has(micmap.mics[mic].role)) {
            $(`#mic_${mic}`).addClass('active role')
            $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
            $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
        }

        // Go through ensemble on page
        if (ensemble.has(micmap.mics[mic].role)) {
            $(`#mic_${mic}`).addClass('active ensemble')
            $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
            $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
        }

        if (state['currentscene']) {
            // Go through all roles in scene
            for (const [index, role] of showdata.scenes[state['currentscene']].roles.entries()) {
                if (role == micmap.mics[mic].role) {
                    $(`#mic_${mic}`).addClass('passive role')
                    $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
                    $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
                }
            }

            // Go through ensemble in scene
            for (const [index, role] of showdata.scenes[state['currentscene']].ensemble.entries()) {
                if (role == micmap.mics[mic].role) {
                    $(`#mic_${mic}`).addClass('passive ensemble')
                    $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
                    $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
                }
            }
        }
    }

}






const goto_page = page => {
    if (page > state['lastpage'])  return
    if (page < state['firstpage']) return

    state['currentpage'] = page
    state['currentscene'] = null
    state['currentmusic'] = null

    let pagehtml  = `<div class='header empty'>(ingen side)</div>`
    let scenehtml = `<div class='header empty'>(ingen scene)</div>`
    let musichtml = `<div class='header empty'>(ingen musikk)</div>`

    if (state['currentpage'] !== null) {
        const sourcepage = showdata.pagemap.find(x => x.target == state['currentpage'])
        const lastpage   = showdata.pagemap.find(x => x.target == state['lastpage'   ])

        pagehtml = `<div class='header'>Side ${sourcepage.source} av ${lastpage.source}</div>`
    }

    for (const scene in showdata.scenes) {
        const start_location = showdata.scenes[scene].start.location.target
        const end_location   = showdata.scenes[scene].end.location.target

        if (start_location < page + 1 && end_location >= page) { state['currentscene'] = parseInt(scene) }
    }

    for (const music in showdata.music) {
        const start_location = showdata.music[music].start.location.target
        const end_location   = showdata.music[music].end.location.target

        if (start_location < page + 1 && end_location >= page) { state['currentmusic'] = parseInt(music) }
    }

    if (state['currentscene'] !== null) { scenehtml = `<div class='header'>${showdata.scenes[state['currentscene']].id} - ${showdata.scenes[state['currentscene']].name}</div>` }
    if (state['currentmusic'] !== null) { musichtml = `<div class='header'>${showdata.music [state['currentmusic']].id} - ${showdata.music [state['currentmusic']].name}</div>` }



    let prev_page  = null, next_page  = null
    let prev_scene = null, next_scene = null
    let prev_music = null, next_music = null

    if (state['currentpage'] !== null) {
        prev_page = state['currentpage' ] - 1
        next_page = state['currentpage' ] + 1
    }

    if (state['currentscene'] !== null) {
        if (state['currentscene'] > 0                         ) { prev_scene = showdata.scenes[state['currentscene'] - 1]?.start?.page.target }
        if (state['currentscene'] < showdata.scenes.length - 1) { next_scene = showdata.scenes[state['currentscene'] + 1]?.start?.page.target }
    } else {
        const prev_scenes = showdata.scenes.filter(scene => scene.start.location.target < page)
        const next_scenes = showdata.scenes.filter(scene => scene.start.location.target > page + 1)

        if (prev_scenes.length) { prev_scene = prev_scenes[-1]?.start?.page.target }
        if (next_scenes.length) { next_scene = next_scenes[ 0]?.start?.page.target }
    }

    if (state['currentmusic'] !== null) {
        if (state['currentmusic'] > 0                        ) { prev_music = showdata.music[state['currentmusic'] - 1]?.start?.page.target }
        if (state['currentmusic'] < showdata.music.length - 1) { next_music = showdata.music[state['currentmusic'] + 1]?.start?.page.target }
    } else {
        const prev_musics = showdata.music.filter(music => music.start.location.target < page    )
        const next_musics = showdata.music.filter(music => music.start.location.target > page + 1)

        if (prev_musics.length) { prev_music = prev_musics[-1]?.start?.page.target }
        if (next_musics.length) { next_music = next_musics[ 0]?.start?.page.target }
    }

    $('.pages > .content' ).html(pagehtml)
    $('.scenes > .content').html(scenehtml)
    $('.music > .content' ).html(musichtml)

    $('.pages > .prev' ).data('page', prev_page)
    $('.pages > .next' ).data('page', next_page)
    $('.scenes > .prev').data('page', prev_scene)
    $('.scenes > .next').data('page', next_scene)
    $('.music > .prev' ).data('page', prev_music)
    $('.music > .next' ).data('page', next_music)

    pdf_render()
    update_miclist()
}






const pdf_load = async pdf => {
    const loadingtask = pdfjsLib.getDocument(pdfdata[pdf])
    state['doc'] = await loadingtask.promise

    state['lastpage']  = state['doc'].numPages
    state['firstpage'] = 1

    goto_page(state['currentpage'])
}






const pdf_render = async () => {
    if (! state['doc']) return

    const page = await state['doc'].getPage(state['currentpage'])

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
}






const set_eventhandlers = () => {
    $(window).on('resize', pdf_render)

    $(document).on('click', '#logout',   () => { window.location.replace('login.php') })

    $(document).on('click', '#toolbar',    event => { event.stopPropagation(); $('.shortcuts').hide() })
    $(document).on('click', '#pdf-viewer', event => { event.stopPropagation(); $('.shortcuts').hide() })
    $(document).on('click', '#infobar',    event => { event.stopPropagation(); $('.shortcuts').hide() })

    $(document).on('click', '#settings', event => { event.stopPropagation(); $('.shortcuts:not(.settings)').hide(); $('.shortcuts.settings').toggle() })
    $(document).on('click', '#print',    event => { event.stopPropagation(); $('.shortcuts:not(.print)'   ).hide(); $('.shortcuts.print'   ).toggle() })

    $(document).on('click', '.scenes > .content', event => { event.stopPropagation(); $('.shortcuts:not(.scenes)').hide(); $('.shortcuts.scenes').toggle() })
    $(document).on('click', '.music > .content',  event => { event.stopPropagation(); $('.shortcuts:not(.music) ').hide(); $('.shortcuts.music' ).toggle() })
    $(document).on('click', '.pages > .content',  event => { event.stopPropagation(); $('.shortcuts:not(.pages) ').hide(); $('.shortcuts.pages' ).toggle() })

    $(document).on('click', '.shortcut', event => { event.stopPropagation(); $('.shortcuts').hide(); goto_page($(event.target).data('page')) })
    $(document).on('click', '.prev',     event => { event.stopPropagation(); $('.shortcuts').hide(); goto_page($(event.target).data('page')) })
    $(document).on('click', '.next',     event => { event.stopPropagation(); $('.shortcuts').hide(); goto_page($(event.target).data('page')) })
}






$(document).ready(async () => {
    await fetch_showdata()

    const show = await get_current_show()

    await populate_show(show)
    await set_eventhandlers()
})
