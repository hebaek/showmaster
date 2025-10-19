import { smlib } from '../modules/smlib.js'
import { data  } from '../modules/data.js'



const render_data = (target, path, json, index = 0): void => {
    const type = path.at(-1)

    const simple_text    = ['text']
    const simple_spans   = ['song', 'character']
    const structure_divs = ['action', 'dialogue']
    const container_divs = ['characters', 'parenthetical', 'lines', 'block', 'line']

    if (simple_text.includes(type)) {
        target.append(json.text)
    }

    else if (simple_spans.includes(type)) {
        target.append(smlib.wrap({ tag: 'span', classes: [type], contents: [json.text] }))
    }

    else if (structure_divs.includes(type)) {
        target.append(smlib.wrap({ tag: 'div', classes: ['content', type] }))
        target = target.children().last()
    }

    else if (container_divs.includes(type)) {
        target.append(smlib.wrap({ tag: 'div', classes: [type] }))
        target = target.children().last()
    }

    else if (type === 'scene') {
        const title_html = smlib.wrap({ tag: 'div', classes: ['title'], contents: [`${json.id} - ${json.name}`] })
        const scene_html = smlib.wrap({ tag: 'div', classes: ['scene'], contents: [title_html], data: { id: json.id } })
        target.append(scene_html)
        target = target.children().last()
    }

    else if (type === 'cues') {
        const cues_html = smlib.wrap({ tag: 'div', classes: ['cues'], data: { 'id': index } })
        target.before(cues_html)
        target = target.prev()
    }

    else if (type === 'music') {
        const data = {}
        if ('id'   in json) data['id']   = json.id
        if ('mode' in json) data['mode'] = json.mode

        const contents = [
            smlib.wrap({ tag: 'div', classes: ['title'], contents: [json.name] })
        ]

        if ('tempo' in json) {
            const html = [`<div class='note'></div>`, `<div class='text'>${json.tempo}</div>`, `<div class='light'></div>`]
            contents.push(smlib.wrap({ tag: 'div', classes: ['metronome'], contents: html, data: { 'tempo': json.tempo } }))

            smlib.add_css(`.cue.music[data-id='${json.id}'] .light { animation: blink calc(60s / ${json.tempo}) infinite; }`)
        }

        target.append(smlib.wrap({ tag: 'div', classes: ['cue', type], contents: contents, data: data }))
        target = target.children().last()
    }


    if (target && 'content' in json) {
        for (const element of json.content) {
            render_data(target, [...path, element.type], element, index+1)
        }
    }
}



const render_manus = (): void => {
    $('#manus').empty()

    render_data($('#manus'), ['manus'], data.manus)
}



const render_cues = (): void => {
    $('.cues').remove()

    let index = 0
    for (const cue of data.cues) {
        const target = $(`.scene[data-id='${cue.scene}']`).children('.content').eq(cue.before)
        render_data(target, ['cues'], cue.content, index++)
    }
}



const create_shortcuts = (): void => {
    $('#navigation').append(`<div class='buttons scenes'><div class='shortcuts scenes'></div><div class='heading'>Scener</div><button class='content'></button><button class='prev'>forrige</button><button class='next'>neste</button></div>`)
    $('#navigation').append(`<div class='buttons music'><div class='shortcuts music'></div><div class='heading'>Musikk</div><button class='content'></button><button class='prev'>forrige</button><button class='next'>neste</button></div>`)

    $('.scene').each(function(index, scene) {
        const name = $(scene).children('.title').first().text()
        const data = {
            id:   $(scene).attr('data-id'),
            type: 'scene',
        }

        $('.shortcuts.scenes').append(smlib.wrap({ tag: 'button', classes: ['shortcut'], contents: [name], data: data }))
    })

    $('.cue.music').each(function(index, music) {
        if ($(music).attr('data-mode') === 'start') {
            const name = $(music).children('.title').first().text()
            const data = {
                id:   $(music).attr('data-id'),
                type: 'music',
            }

            $('.shortcuts.music').append(smlib.wrap({ tag: 'button', classes: ['shortcut'], contents: [name], data: data }))
        }
    })
}



const get_active = (): void => {
    const id = smlib.get_active()

    $('.scenes > .content').html($(`.scene[data-id='${id.scene.current}'] > .title`).text())
    $('.scenes > .prev').attr('data-type', 'scene')
    $('.scenes > .next').attr('data-type', 'scene')
    $('.scenes > .prev').attr('data-id', id.scene.prev)
    $('.scenes > .next').attr('data-id', id.scene.next)

    $('.music > .content').html($(`.music[data-id='${id.music.current}'] > .title`).text())
    $('.music > .prev').attr('data-type', 'music')
    $('.music > .next').attr('data-type', 'music')
    $('.music > .prev').attr('data-id', id.music.prev)
    $('.music > .next').attr('data-id', id.music.next)
}



function update_data(cues) {
    const scene_id = $(cues).parents('.scene').first().attr('data-id')
    const cues_id  = $(cues).attr('data-id')
    const index    = $(cues).index() - 1

    const after = $(cues).prev()
console.log(after)

    data.cues[cues_id].scene = scene_id
    data.cues[cues_id].before = index

    $('#save_cues').show()
    $('#revert_cues').show()
}



const make_draggable = () => {
    $('.scene').sortable({
        axis: 'y',
        connectWith: '.scene',
        items: '> .cues, > .content',
        cancel: '.content',
        placeholder: 'cues-placeholder',
        start: function(event, ui) {
            ui.placeholder.height(ui.helper.outerHeight())
        },
        update: function(event, ui) {
            const cues = ui.item
            update_data(cues)
        },
        sort: function(event, ui) {
            const scene = ui.placeholder.closest('.scene')
            const title = scene.find('.title').first()

            if (ui.placeholder.index() <= title.index()) {
                ui.placeholder.insertAfter(title)
            }
        }
    })

    $('.scene').disableSelection()
}



const setup_events = (): void => {
    $(document).on('click', '.shortcut', event => { $('.shortcuts').hide(); goto_id($(event.target).attr('data-type'), $(event.target).attr('data-id')) })
    $(document).on('click', '.prev',     event => { $('.shortcuts').hide(); goto_id($(event.target).attr('data-type'), $(event.target).attr('data-id')) })
    $(document).on('click', '.next',     event => { $('.shortcuts').hide(); goto_id($(event.target).attr('data-type'), $(event.target).attr('data-id')) })

    $('#manus').on('scroll', () => { get_active() })
}



const goto_id = (type, id): void => {
    if (type === 'scene') {
        const target = $(`#manus .scene[data-id='${id}']`)[0]
        target.scrollIntoView({ behavior: 'smooth' })
    }

    if (type === 'music') {
        const target = $(`#manus .music[data-id='${id}']`)[0]
        target.scrollIntoView({ behavior: 'smooth' })
    }
}



export const setup = async (): Promise<void> => {
    await data.load({ content: 'manus', revision: '1' })
    await data.load({ content: 'cues' })

    const html: string = smlib.wrap({ tag: 'div', id: 'manus' })
    smlib.append($(document.body), html)

    render_manus()
    render_cues()
    create_shortcuts()

    $('#manus .scene').sortable({
        axis: 'y',
        connectWith: '.scene', // Allow sorting between scenes
        items: '> .cues, > .content', // Sortable items
        cancel: '.content', // Prevent sorting for content
        placeholder: 'cues-placeholder' // Placeholder style
    }).disableSelection();

    const pos = localStorage.getItem('scroll_position')
    if (pos) { $('#manus').scrollTop(parseInt(pos)) }

//    make_draggable()

    get_active()
    setup_events()


    seteditable()
}







const seteditable = () => {
    $('.metronome .text').on('click', event => {
        const textDiv = $(event.target)
        const metronome = textDiv.closest('.metronome')
        const id = $(event.target).parentsUntil('.music').parent().attr('data-id')

        const oldTempo = textDiv.text()
        let newTempo = oldTempo

        textDiv.attr('contenteditable', 'true').addClass('editing').focus()

        const range = document.createRange()
        const selection = window.getSelection()

        range.selectNodeContents(textDiv.first()[0])
        range.collapse(false)

        selection.removeAllRanges()
        selection.addRange(range)

        textDiv.on('keydown', e => {
            if (e.key === 'Enter') {
                e.preventDefault()
                newTempo = textDiv.text()
                metronome.data('tempo', newTempo)
                textDiv.removeClass('editing').attr('contenteditable', 'false').text(newTempo)

                set_tempo(id, newTempo)
            } else if (e.key === 'Escape') {
                e.preventDefault();
                textDiv.removeClass('editing').attr('contenteditable', 'false').text(oldTempo)
            } else if (e.key >= '0' && e.key <= '9') {
            } else if (e.key === 'Backspace') {
            } else if (e.key === 'ArrowLeft') {
            } else if (e.key === 'ArrowRight') {
            } else {
                e.preventDefault()
            }
        })

        textDiv.on('blur', e => {
            e.preventDefault()
            newTempo = textDiv.text()
            metronome.data('tempo', newTempo)
            textDiv.removeClass('editing').attr('contenteditable', 'false').text(newTempo)

            set_tempo(id, newTempo)
        })
    })

    const set_tempo = (id, tempo) => {
        smlib.add_css(`.cue.music[data-id='${id}'] .light { animation: blink calc(60s / ${tempo}) infinite; }`)
    }
}
