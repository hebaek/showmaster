const projectfile = 'data/shows.json'
const projectdata = {}
const pdfdata     = {}

let showdata = null

const serverdata  = {
    'read':  false,
    'write': false,
}

const state = {
    'firstpage':    null,
    'lastpage':     null,

    'currentpage':  null,
    'currentscene': null,
    'currentmusic': null,

    'doc':          null,

    'renderer':     null,
}






const fetch_showdata = async () => {
    try {
        const response = await fetch(projectfile)
        if (!response.ok) { throw new Error('Feil ved lasting av showdata') }

        const shows = await response.json()

        for (const show in shows.showdata) {
            projectdata[show] = {
                'url':    shows.showdata[show].url,
                'name':   shows.showdata[show].name,
                'date':   shows.showdata[show].date,
                'time':   shows.showdata[show].time,
                'durata': shows.showdata[show].durata,
            }
        }

        show = await get_current_show()

        for (const pdf of ['empty', 'music', 'mics']) {
            pdfdata[pdf] = {
                'url':  shows.pdf[pdf].url,
                'name': shows.pdf[pdf].name,
            }
        }

        for (const pdf in shows.pdf[show]) {
            pdfdata[pdf] = {
                'url':  shows.pdf[show][pdf].url,
                'name': shows.pdf[show][pdf].name,
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
    const now = new Date(Date.now())

    for (const show in projectdata) {
        const date   = projectdata[show].date
        const time   = projectdata[show].time
        const durata = projectdata[show].durata

        const starttime = new Date(`${date}T${time}`)
        const endtime   = new Date(`${date}T${time}`)
        const h = new Date(`${date}T${durata}`).getHours()
        const m = new Date(`${date}T${durata}`).getMinutes()
        const s = new Date(`${date}T${durata}`).getSeconds()

        endtime.setTime(endtime.getTime() + h * 60*60*1000)
        endtime.setTime(endtime.getTime() + m *    60*1000)
        endtime.setTime(endtime.getTime() + s *       1000)

        if (endtime > now) {
            return show
        }
    }
}






const populate_show = async show => {
    showdata = await load_show(show)

    pdf_load('mics')

    create_shortcuts(showdata)
    create_miclist(showdata)
}






const create_shortcuts = () => {
    $('.shortcuts.print').append(`<div class='heading'>Manus</div>`)

    for (pdf of ['empty', 'music', 'mics']) {
        let url  = `${pdfdata[pdf].url}`
        let text = `${pdfdata[pdf].name}`
        $('.shortcuts.print').append(`<button class='pdf' data-url='${url}'>${text}</button>`)
    }

    $('.shortcuts.print').append(`<div class='heading'>Mikrofonlister</div>`)
    for (pdf of ['actor:mic/role', 'role:mic/actor', 'mic:actor/role', 'mic:role/actor']) {
        let url  = `${pdfdata[pdf].url}`
        let text = `${pdfdata[pdf].name}`
        $('.shortcuts.print').append(`<button class='pdf' data-url='${url}'>${text}</button>`)
    }



    showdata.scenes.forEach(scene => {
        let classes = 'shortcut'
        let text = `${scene.id} - ${scene.name}`

        $('.shortcuts.scenes').append(`<button class='${classes}' data-page='${scene.start.page.target}'>${text}</button>`)
    })

    showdata.music.forEach(music => {
        let classes = 'shortcut'
        if (music.type == 'instrumental') { classes += ' instrumental' }
        if (music.type == 'dialog'      ) { classes += ' dialog'       }
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
    const micmap = showdata.micmap.filter(row => row.location.target < state['currentpage'] + 0.01).pop()
    const lines = showdata.lines.filter(line => line.location.target < state['currentpage'] + 1 && line.location.target >= state['currentpage'])
    const roles    = new Set(lines.map(line => line.roles   ).reduce((result, roles) => [...result, ...roles], []))
    const ensemble = new Set(lines.map(line => line.ensemble).reduce((result, roles) => [...result, ...roles], []))

    $('.row').removeClass('passive_role passive_ensemble active_role active_ensemble choir')
    $('.row > .role').html('')
    $('.row > .actor').html('')

    for (const mic in micmap.mics) {
        let choirclass = ''
        if (micmap.mics[mic].actor == 'Kor') { choirclass = 'choir' }

        // Go through all roles on page
        if (roles.has(micmap.mics[mic].role)) {
            $(`#mic_${mic}`).addClass('active_role')
            $(`#mic_${mic}`).addClass(choirclass)
            $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
            $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
        }

        // Go through ensemble on page
        if (ensemble.has(micmap.mics[mic].role)) {
            $(`#mic_${mic}`).addClass('active_ensemble')
            $(`#mic_${mic}`).addClass(choirclass)
            $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
            $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
        }

        if (state['currentscene']) {
            // Go through all roles in scene
            for (const [index, role] of showdata.scenes[state['currentscene']].roles.entries()) {
                if (role == micmap.mics[mic].role) {
                    $(`#mic_${mic}`).addClass('passive_role')
                    $(`#mic_${mic}`).addClass(choirclass)
                    $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
                    $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
                }
            }

            // Go through ensemble in scene
            for (const [index, role] of showdata.scenes[state['currentscene']].ensemble.entries()) {
                if (role == micmap.mics[mic].role) {
                    $(`#mic_${mic}`).addClass('passive_ensemble')
                    $(`#mic_${mic}`).addClass(choirclass)
                    $(`#mic_${mic} > .role` ).html(micmap.mics[mic].role )
                    $(`#mic_${mic} > .actor`).html(micmap.mics[mic].actor)
                }
            }
        }
    }

}






const download = url => {
    window.open(url)
}






const handle_keypress = event => {
    console.log(event.originalEvent.code)
    switch (event.originalEvent.code) {
        case 'ArrowLeft':
        case 'PageUp':
        case 'Backspace':
            page = $('.pages > .prev').data('page')
            goto_page('write', page)
            break

        case 'ArrowRight':
        case 'PageDown':
        case 'Space':
            page = $('.pages > .next').data('page')
            goto_page('write', page)
            break

        case 'ArrowUp':
            page = $('.scenes > .prev').data('page')
            goto_page('write', page)
            break

        case 'ArrowDown':
            page = $('.scenes > .next').data('page')
            goto_page('write', page)
            break

        case 'Enter':
            server_toggle('read')
            server_toggle('write')
            break
    }
}






const goto_page = (mode, page) => {
    if (page > state['lastpage'])  return
    if (page < state['firstpage']) return

    if (mode == 'write' && serverdata['write'] == true) { server_setpage(page) }

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

        if (start_location < page + 1 && end_location >= page) {
            state['currentscene'] = parseInt(scene)
            break
        }
    }

    for (const music in showdata.music) {
        const start_location = showdata.music[music].start.location.target
        const end_location   = showdata.music[music].end.location.target

        if (start_location < page + 1 && end_location >= page) {
            state['currentmusic'] = parseInt(music)
            break
        }
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


    const prev_scenes = showdata.scenes.filter(scene => scene.end.location.target < page)
    const next_scenes = showdata.scenes.filter(scene => scene.start.location.target > page + 1)
    if (prev_scenes.length) { prev_scene = prev_scenes[prev_scenes.length - 1]?.start?.page.target }
    if (next_scenes.length) { next_scene = next_scenes[0]?.start?.page.target }


    const prev_musics = showdata.music.filter(music => music.end.location.target < page)
    const next_musics = showdata.music.filter(music => music.start.location.target > page + 1)
    if (prev_musics.length > 0) { prev_music = prev_musics[prev_musics.length - 1]?.start?.page.target }
    if (next_musics.length > 0) { next_music = next_musics[ 0]?.start?.page.target }


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
    const loadingtask = pdfjsLib.getDocument(pdfdata[pdf].url)
    state['doc'] = await loadingtask.promise

    state['lastpage']  = state['doc'].numPages
    state['firstpage'] = 1

    goto_page('read', state['currentpage'])
}






const pdf_render = async () => {
    if (! state['doc']) return

    const page = await state['doc'].getPage(state['currentpage'])

    const canvas = document.getElementById('pdf-canvas')
    const context = canvas.getContext('2d')

    const desiredWidth  = $('#pdf').innerWidth()
    const desiredHeight = $('#pdf').innerHeight()

    const testViewport = page.getViewport({ scale: 4.0 })

    const scaleWidth  = desiredWidth  / testViewport.width
    const scaleHeight = desiredHeight / testViewport.height
    const scale = Math.min(scaleWidth, scaleHeight)

    var viewport = page.getViewport({ scale: 4 * scale })
    canvas.height = 4 * viewport.height
    canvas.width  = 4 * viewport.width

    canvas.style.height = viewport.height + 'px'
    canvas.style .width = viewport.width  + 'px'

    viewportHeight = viewport.height
    viewportWidth = viewport.width

    var renderContext = {
        canvasContext: context,
        viewport: viewport,
        transform: [4, 0, 0, 4, 0, 0],
    }

    if (!state['renderer']) {
        state['renderer'] = page.render(renderContext)

        try {
            await state['renderer'].promise
        } catch (error) {
            if (error.name === "RenderingCancelledException") { console.log("Render cancelled.")       }
            else                                              { console.error("Render failed:", error) }
        } finally {
            state['renderer'] = null
        }
    } else {
        state['renderer'].cancel()
        state['renderer'] = null
        setTimeout(pdf_render, 10)
    }
}





/*
const pdf_list_show = pdf => {
    const url = pdfdata[pdf].url
    $('#pdf-viewer').attr('src', url)

    $('#pdf-viewer').show()
    $('#infobar').hide()
}

const pdf_list_hide = () => {
    $('#pdf-viewer').hide()
    $('#infobar').show()
}
*/





const set_eventhandlers = () => {
    $(window).on('resize', pdf_render)

    $(document).on('click', '#logout',   () => { window.location.replace('login.php') })

    $(document).on('click', '#toolbar',  event => { event.stopPropagation(); $('.shortcuts').hide() })
    $(document).on('click', '#pdf',      event => { event.stopPropagation(); $('.shortcuts').hide() })
    $(document).on('click', '#infobar',  event => { event.stopPropagation(); $('.shortcuts').hide() })

    $(document).on('click', '#settings', event => { event.stopPropagation(); $('.shortcuts:not(.settings)').hide(); $('.shortcuts.settings').toggle() })
    $(document).on('click', '#print',    event => { event.stopPropagation(); $('.shortcuts:not(.print)'   ).hide(); $('.shortcuts.print'   ).toggle() })

    $(document).on('click', '#write',    event => { event.stopPropagation(); server_toggle('write') })
    $(document).on('click', '#read',     event => { event.stopPropagation(); server_toggle('read' ) })

    $(document).on('click', '.pdf', event => { event.stopPropagation(); $('.shortcuts').hide(); download($(event.target).data('url')) })

    $(document).on('click', '.scenes > .content', event => { event.stopPropagation(); $('.shortcuts:not(.scenes)').hide(); $('.shortcuts.scenes').toggle() })
    $(document).on('click', '.music > .content',  event => { event.stopPropagation(); $('.shortcuts:not(.music) ').hide(); $('.shortcuts.music' ).toggle() })
    $(document).on('click', '.pages > .content',  event => { event.stopPropagation(); $('.shortcuts:not(.pages) ').hide(); $('.shortcuts.pages' ).toggle() })

    $(document).on('click', '.shortcut', event => { event.stopPropagation(); $('.shortcuts').hide(); goto_page('write', $(event.target).data('page')) })
    $(document).on('click', '.prev',     event => { event.stopPropagation(); $('.shortcuts').hide(); goto_page('write', $(event.target).data('page')) })
    $(document).on('click', '.next',     event => { event.stopPropagation(); $('.shortcuts').hide(); goto_page('write', $(event.target).data('page')) })

    $(document).on('keydown', event => { event.stopPropagation(); handle_keypress(event) })



//    $(document).on('click', '#settings', event => { event.stopPropagation(); $('.shortcuts:not(.settings)').hide(); $('.shortcuts.settings').toggle(); pdf_list_show('actor:mic/role') })
//    $(document).on('click', '#print',    event => { event.stopPropagation(); $('.shortcuts:not(.print)'   ).hide(); $('.shortcuts.print'   ).toggle(); pdf_list_hide() })
}






const server_toggle = mode => {
    if (mode == 'write') { serverdata['write'] = !serverdata['write'] }
    if (mode == 'read' ) { serverdata['read' ] = !serverdata['read' ]; server_poll() }

    for (const mode of ['write', 'read']) {
        if (serverdata[mode]) {
            $(`#${mode}`).removeClass('disabled')
        } else {
            $(`#${mode}`).addClass('disabled')
        }
    }
}

const server_getpage = () => {
    fetch('getpage.php')
    .then(response => response.text())
    .then(page => {
        $('#read').addClass('sync')
        setTimeout(() => $('#read').removeClass('sync error'), 250)

        const pageNumber = parseInt(page, 10);
        if (!isNaN(pageNumber) && pageNumber !== state['currentpage']) {
            goto_page('read', pageNumber)
        }
    })
    .catch(error => {
        console.error('Error getting page:', error)
        $('#read').addClass('error')
    })
}

const server_setpage = page => {
    fetch('setpage.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `page=${page}`,
    })
    .then(response => response.text())
    .then(message => console.log(message))
    .then(() => {
        $('#write').addClass('sync')
        setTimeout(() => $('#write').removeClass('sync error'), 250)
    })
    .catch(error => {
        console.error('Error setting page:', error)
        $('#write').addClass('error')
    })
}

const server_poll = () => {
    if (serverdata['read']) {
        server_getpage()
        setTimeout(server_poll, 1000)
    }
}




$(document).ready(async () => {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.9.179/pdf.worker.min.js'

    await fetch_showdata()

    const show = await get_current_show()

    await populate_show(show)
    await set_eventhandlers()

    server_poll()
})
