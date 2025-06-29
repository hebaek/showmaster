import { flags } from './flags.js'



/******************************************************************************
/
/   Type definitions
/
/*****************************************************************************/

type Ids = {
    current?: string;
    next?:    string;
    prev?:    string;
}



type Modules = {
    [key: string]: { enable: boolean; file: string; };
}



/******************************************************************************
/
/   Implementation
/
/*****************************************************************************/

const modules = (): Modules => {
    return flags.modules
}



const test_flags = (tests: string[]): boolean => {
    for (const test of tests) {
        if (test === 'data') continue
        if (test === 'load') continue
    }

    return true
}



const get_active = (): { scene: Ids, music: Ids } => {
    const pos = $('#manus').scrollTop()
    localStorage.setItem('scroll_position', pos.toString())

    const result = {
        scene: { current: undefined, next: undefined, prev: undefined },
        music: { current: undefined, next: undefined, prev: undefined },
    }

    const midpoint = $('#manus').innerHeight() / 2

    const scene = $('.scene')
    scene.each(function(index) {
        const y = $(this).position().top
        if (y > midpoint) return

        const index_prev = index     > 0               ? index - 1 : index
        const index_next = index + 1 < $(scene).length ? index + 1 : index

        result.scene.current = $(this).attr('data-id')
        result.scene.next    = $(scene).eq(index_next).attr('data-id')
        result.scene.prev    = $(scene).eq(index_prev).attr('data-id')
    })

    const music = $('.cue.music[data-mode="start"]')
    music.each(function(index) {
        const y = $(this).position().top
        if (y > midpoint) return

        const index_prev = index     > 0               ? index - 1 : index
        const index_next = index + 1 < $(music).length ? index + 1 : index

        result.music.current = $(this).attr('data-id')
        result.music.prev    = $(music).eq(index_prev).attr('data-id')
        result.music.next    = $(music).eq(index_next).attr('data-id')
    })

    return result
}



const wrap = (params: {
    tag: string,
    id?: string,
    classes?:  readonly string[],
    contents?: readonly string[],
    attrs?:    Record<string, string|number>,
    data?:     Record<string, string|number>,
}): string => {
    const tag      = params.tag
    const id       = 'id'       in params ? ` id="${params.id}"`                                                       : ''
    const classes  = 'classes'  in params ? ` class="${params.classes.join(' ')}"`                                     : ''
    const contents = 'contents' in params ? params.contents.join('')                                                   : ''
    const attrs    = 'attrs'    in params ? Object.entries(params.attrs).map(([k, v]) => `${k}="${v}"`).join(' ')      : ''
    const data     = 'data'     in params ? Object.entries(params.data ).map(([k, v]) => `data-${k}="${v}"`).join(' ') : ''

    return `<${tag}${id}${classes}${attrs}${data}>${contents}</${tag}>`
}



const append = (
    target: JQuery,
    html:   string,
): void => {
    $(target).append(html)
}



const add_css = (
    rule: string,
): void => {
    const stylesheet = document.styleSheets[0]
    stylesheet.insertRule(rule, stylesheet.cssRules.length)
}



/******************************************************************************
/
/   Module exports
/
/*****************************************************************************/

export const smlib = {
    modules:    modules,
    test_flags: test_flags,
    get_active: get_active,
    wrap:       wrap,
    append:     append,
    add_css:    add_css,
    pdfjsLib:   undefined,
}
