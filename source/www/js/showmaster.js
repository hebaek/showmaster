const state = {
    'pdffile':      null,

    'firstpage':    null,
    'lastpage':     null,

    'currentpage':  null,
    'currentscene': null,
    'currentmusic': null,

    'doc':          null,
}



const load_manus = async file => {
    try {
        const response = await fetch(file)
        if (!response.ok) throw new Error('Feil ved lasting av manus')
        return response.json()
    } catch (error) {
        console.error('Klarte ikke å laste manus:', error)
    }
}



const render = (target, path, json) => {
    let container = target

    if (path.endsWith('/scene')) {
        container = $('<div>')
        target.append(container)

        container.addClass('scene')
        container.attr('id', json.id)

        const title = $('<div>')
        title.addClass('title')
        title.text(`${json.id} - ${json.name}`)

        container.append(title)
    }


    else if (path.endsWith('/cues')) {
        container = $('<div>')
        container.addClass('cues')
        target.append(container)
    }

    else if (path.endsWith('/cues/music')) {
        container = $('<div>')
        container.addClass('music')
        target.append(container)

        if (Object.hasOwn(json, 'id'))   container.attr('id', 'music_' + json.id)
        if (Object.hasOwn(json, 'name')) container.attr('name', json.name)

        if (Object.hasOwn(json, 'pdf')) {
            button = $('<div>')
            button.addClass('button')
            button.data('file', json.pdf.filename)
            button.data('page', json.pdf.page)
            button.text('Last PDF')


            container.append(button)
        }
    }

    else if (path.endsWith('/action')) {
        container = $('<div>')
        container.addClass('action')
        target.append(container)
    }

    else if (path.endsWith('/dialogue')) {
        container = $('<div>')
        container.addClass('dialogue')
        target.append(container)
    }

    else if (path.endsWith('/characters')) {
        container = $('<div>')
        container.addClass('characters')
        target.append(container)
    }
    else if (path.endsWith('/parenthetical')) {
        container = $('<div>')
        container.addClass('parenthetical')
        target.append(container)
    }

    else if (path.endsWith('/lines')) {
        container = $('<div>')
        container.addClass('lines')
        target.append(container)
    }

    else if (path.endsWith('/block')) {
        container = $('<div>')
        container.addClass('block')
        target.append(container)
    }

    else if (path.endsWith('/line')) {
        container = $('<div>')
        container.addClass('line')
        target.append(container)
    }

    else if (path.endsWith('/text')) {
        target.append(json.text)
    }

    else if (path.endsWith('/song')) {
        container = $('<span>')
        target.append(container)

        container.addClass('song')
        container.append(json.text)
    }

    else if (path.endsWith('/line/cue')) {
        container = $('<span>')
        target.append(container)

        container.addClass('cue')
        container.append(json.text)
    }

    else if (path.endsWith('/character')) {
        container = $('<span>')
        target.append(container)

        container.addClass('character')
        container.append(json.text)
    }



    if (container && Object.hasOwn(json, 'content')) {
        for (const element of json.content) {
            render(container, path + '/' + element.type, element)
        }
    }
}



const addshortcuts = manus => {
    manus.content.forEach(element => {
        if (element.type === 'scene') {
            const name = `${element.id} - ${element.name}`
            $('.shortcuts.scenes').append(`<button class='shortcut' data-id='${element.id}'>${element.id} - ${element.name}</button>`)
        }
    })

    $('.cues > .music').each(function(index) {
        if (this) {
            const id   = $(this).attr('id')   || null
            const name = $(this).attr('name') || 'noname'

            if (id) {
                $('.shortcuts.music').append(`<button class='shortcut' data-id='${id}'>${name}</button>`)
            }
        }
    })
}



const get_active_scene = manus => {
    const height = $('#manus').innerHeight() / 2

    let id = null
    let i = null

    $('.scene').each(function(index)  {
        let y = $(this).position().top
        if (y > height) return

        id = $(this).attr('id')
        i = index
    })

    const scenehtml = $(`#${id} > .title`).text()
    $('.scenes > .content').html(scenehtml)
}



const goto_id = id => {
    const anchor = document.getElementById(id)
    anchor.scrollIntoView({ behavior: 'smooth' })
}



const handle_keypress = event => {
    switch (event.originalEvent.code) {
        case 'ArrowLeft':
            if (state['currentpage'] > state['firstpage']) {
                state['currentpage'] -= 1
                pdf_render()
            }
            break

        case 'ArrowRight':
            if (state['currentpage'] < state['lastpage']) {
                state['currentpage'] += 1
                pdf_render()
            }
            break

        case 'PageUp':
            break

        case 'Backspace':
            break

        case 'PageDown':
            break

        case 'Space':
            break

        case 'ArrowUp':
            $('#manus').animate({
                scrollTop: $('#manus').scrollTop() - $('#manus').innerHeight() / 2
            }, 300)
            break

        case 'ArrowDown':
            $('#manus').animate({
                scrollTop: $('#manus').scrollTop() + $('#manus').innerHeight() / 2
            }, 300)
            break

        case 'Enter':
            break
    }
}



const handle_button = async event => {
    const id   = $(event.target).parent().attr('id')
    const name = $(event.target).parent().attr('name')

    const file = $(event.target).data('file')
    const page = $(event.target).data('page')

    $('.music > .content').html(name)

    if (file !== state['pdffile']) {
        state['pdffile'] = file
        await pdf_load()
    }

    state['currentpage'] = page

    pdf_render()
}



const handle_rightclick = event => {
    const target = event.target

    const menu = $('#contextmenu')

    const mouseX = event.pageX
    const mouseY = event.pageY

    const menuWidth = menu.outerWidth()
    const menuHeight = menu.outerHeight()
    const viewportWidth = $(window).width()
    const viewportHeight = $(window).height()

    let adjustedX = mouseX
    let adjustedY = mouseY

    if (mouseX + menuWidth > viewportWidth) {
        adjustedX = viewportWidth - menuWidth - 10
    }
    if (mouseY + menuHeight > viewportHeight) {
        adjustedY = viewportHeight - menuHeight - 10
    }

    if (adjustedX < 0) adjustedX = 10
    if (adjustedY < 0) adjustedY = 10

    const parentlist = []
    parentlist.push($(target).attr('class').split(' ')[0])

    const parents = $(target).parentsUntil('#manus')
    parents.each(function(index) {
        const parent = $(this).attr('class').split(' ')[0]
        parentlist.push(parent)
    })
    console.log(parentlist)

    const elements = new Set()

    if (parentlist.includes('cues'))     { elements.add(`<div id='cue_add'>Add cue</div>`) }
    if (parentlist.includes('block'))    { elements.add(`<div id='cue_add_before'>Add cue before</div>`) }
    if (parentlist.includes('dialogue')) { elements.add(`<div id='cue_add_before'>Add cue before</div>`) }
    if (parentlist.includes('title'))    { elements.add(`<div id='cue_add_after'>Add cue after</div>`) }
    if (parentlist.includes('block'))    { elements.add(`<div id='cue_add_after'>Add cue after</div>`) }
    if (parentlist.includes('dialogue')) { elements.add(`<div id='cue_add_after'>Add cue after</div>`) }
    if (parentlist.includes('music'))    { elements.add(`<div id='cue_remove'>Remove cue</div>`) }
    if (parentlist.includes('cues'))     { elements.add(`<div id='cues_remove'>Remove all cues</div>`) }

    console.log([...elements])
    $('#contextmenu').html([...elements].join(''))

    menu.css({ top: `${adjustedY}px`, left: `${adjustedX}px` }).fadeIn(200)

    $(document).on('click', '#contextmenu > div', event => { $(document).off('click', '#contextmenu > div'); handle_contextclick(target, event) })
    $(document).one('click', event => { $(document).off('click', '#contextmenu > div'); menu.hide() })
}



const handle_contextclick = (target, event) => {
    const id = $(event.target).attr('id')

    if (id === 'cue_add') {
        const element = $(target).parents('.block, .dialogue, .action').first()
        element.before('<div class="cues">Hello...</div>')
    }

    if (id === 'cue_remove') {
        if ($(target).hasClass('cues')) {
            $(target).remove()
        } else {
            const element = $(target).parents('.cues').first()
            element.remove()
        }
    }
}



const set_eventhandlers = () => {
    $(document).on('click', '#logout',   () => { window.location.replace('login.php') })

    $(document).on('click', '.scenes > .content', event => { $('.shortcuts:not(.scenes)').hide(); $('.shortcuts.scenes').toggle() })
    $(document).on('click', '.music > .content',  event => { $('.shortcuts:not(.music) ').hide(); $('.shortcuts.music' ).toggle() })

    $(document).on('click', '.shortcut', event => { $('.shortcuts').hide(); goto_id($(event.target).data('id')) })
    $(document).on('click', '.prev',     event => { $('.shortcuts').hide(); goto_id($(event.target).data('id')) })
    $(document).on('click', '.next',     event => { $('.shortcuts').hide(); goto_id($(event.target).data('id')) })

    $(document).on('click', '.button',   event => { handle_button(event) })

    $('#manus').on('contextmenu', event => { event.preventDefault(); handle_rightclick(event) })
    $(document).on('keydown',     event => { event.preventDefault(); handle_keypress(event) })

    $('#manus').on('scroll', event => { get_active_scene() })
}



$(document).ready(async () => {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.9.179/pdf.worker.min.js'

    const manus = await load_manus('data/manus.json')

    render($('#manus'), 'manus', manus)
    addshortcuts(manus)

    set_eventhandlers()

    goto_id($('.scene')[0].id)
})



















const pdf_load = async () => {
    const loadingtask = pdfjsLib.getDocument('data/sheetmusic/' + state['pdffile'])
    state['doc'] = await loadingtask.promise

    state['lastpage']  = state['doc'].numPages
    state['firstpage'] = 1
    state['currentpage'] = 1
}






const pdf_render = async () => {
    if (! state['doc']) return

    const page  = await state['doc'].getPage(state['currentpage'])

    $('#pdf').html(`<canvas id='pdf-page'></canvas>`)

    const canvas = document.getElementById('pdf-page')
    const context = canvas.getContext('2d')

    const desiredWidth   = $('#pdf').innerWidth()
    const desiredHeight  = $('#pdf').innerHeight()

    const testViewport = page.getViewport({ scale: 4.0 })

    const scaleWidth  = desiredWidth  / testViewport.width
    const scaleHeight = desiredHeight / testViewport.height
    const scale = Math.min(scaleWidth, scaleHeight)

    var viewport = page.getViewport({ scale: 4 * scale })

    canvas.height = 4 * viewport.height
    canvas.width  = 4 * viewport.width

    canvas.style.height = viewport.height + 'px'
    canvas.style .width = 'calc(' + viewport.width  + 'px - 0.5em)'

    const viewportHeight = viewport.height
    const viewportWidth = viewport.width

    var renderContext = {
        canvasContext: context,
        viewport: viewport,
        transform: [4, 0, 0, 4, 0, 0],
    }


    page.render(renderContext)
}
