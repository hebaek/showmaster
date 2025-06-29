import { smlib } from '../modules/smlib.js'



const setup_events = (): void => {
    $(document).on('click', '.scenes > .content', () => { $('.shortcuts:not(.scenes)').hide(); $('.shortcuts.scenes').toggle() })
    $(document).on('click', '.music > .content',  () => { $('.shortcuts:not(.music) ').hide(); $('.shortcuts.music' ).toggle() })

    $(document).on('click', '#toolbar', () => {
        $('#toolbar').toggleClass('collapsed')
        const collapsed = $('#toolbar').hasClass('collapsed') ? 'true' : 'false'
        localStorage.setItem('menu-collapsed', collapsed)

        if (collapsed === 'true') { $(':root').css("--toolbar-width", "var(--toolbar-width-closed)") }
        else                      { $(':root').css("--toolbar-width", "var(--toolbar-width-open)")   }
    })
}



export const setup = async (): Promise<void> => {
    const contents: string[] = [
        smlib.wrap({ tag: 'div', id: 'navigation' })
    ]

    const html: string = smlib.wrap({ tag: 'div', id: 'toolbar', contents: contents })
    smlib.append($(document.body), html)

    setup_events()

    const collapsed = localStorage.getItem('menu-collapsed') === 'true'
    if (collapsed) $('#toolbar').addClass('collapsed')

    if (collapsed) { $(':root').css("--toolbar-width", "var(--toolbar-width-closed)") }
    else           { $(':root').css("--toolbar-width", "var(--toolbar-width-open)")   }
}
