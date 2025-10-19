import { smlib } from '../modules/smlib.js'



/******************************************************************************
/
/   Type definitions
/
/*****************************************************************************/

type PDFPageProxy = {
    getViewport: (params: { scale: number }) => PDFPageViewport;
    render: (params: RenderParams) => any;
}

type PDFPageViewport = {
    width: number;
    height: number;
    scale: number;
}

type RenderParams = {
    canvasContext: CanvasRenderingContext2D;
    viewport: PDFPageViewport;
    transform?: [number, number, number, number, number, number];
}

type RenderContext = {
    canvasContext: CanvasRenderingContext2D;
    viewport: PDFPageViewport;
    transform: [number, number, number, number, number, number];
}



/******************************************************************************
/
/   Implementation
/
/*****************************************************************************/

const json_parse = data => {
    const result = new Map()

    for (const song of data) {
        song.id = song.id.toString()

        result.set(song.id, {
            'id': song.id,
            'name': song.name,
            'pdf': {
                'filename': song.pdf.filename,
                'pdf': null,
                'pagecount': 0,
            }
        })
    }

    return result
}



const pdf_scale = (
    page:    PDFPageProxy,
    canvas:  HTMLCanvasElement,
    context: CanvasRenderingContext2D,
): RenderContext => {
    const testViewport = page.getViewport({ scale: 4.0 })
    const scale = $('#pdf').innerHeight() / testViewport.height

    var viewport = page.getViewport({ scale: 4 * scale })

    canvas.height = 4 * viewport.height
    canvas.width  = 4 * viewport.width

    canvas.style.height = viewport.height + 'px'
    canvas.style.width  = viewport.width  + 'px'

    return {
        canvasContext: context,
        viewport: viewport,
        transform: [4, 0, 0, 4, 0, 0],
    }
}



const pdf_load = async (sheetmusic): Promise<void> => {
    const loadingPromises = []

    sheetmusic.forEach((data, id) => {
        const promise = (async () => {
            try {
                const loadingTask = smlib.pdfjsLib.getDocument(data.pdf.filename)
                const pdf = await loadingTask.promise

                data.pdf.pdf = pdf
                data.pdf.pagecount = pdf.numPages
            } catch (error) {
                console.error(`Error loading PDF for id ${id}:`, error);
            }
        })()

        loadingPromises.push(promise)
    })

    await Promise.all(loadingPromises)
}



const pdf_render = async (sheetmusic): Promise<void> => {
    const renderPromises = []

    sheetmusic.forEach(music => {
        for (let pagenumber = 1; pagenumber <= music.pdf.pagecount; pagenumber++) {
            const pdf_page = $('<div>')
            pdf_page.addClass('pdf_page')
            pdf_page.attr('data-pdf-id', music.id)
            pdf_page.attr('data-pdf-page', pagenumber)

            const pdf_canvas = $('<canvas>')

            pdf_page.append(pdf_canvas)
            $('#pdf').append(pdf_page)

            const renderPromise = (async () => {
                const canvas  = $(`.pdf_page[data-pdf-id='${music.id}'][data-pdf-page='${pagenumber}'] canvas`).get(0) as HTMLCanvasElement
                const context = canvas.getContext('2d')
                const page    = await music.pdf.pdf.getPage(pagenumber)

                const renderContext = pdf_scale(page, canvas, context)
                page.render(renderContext)

                $(canvas).innerWidth(renderContext.viewport.width)
            })()

            renderPromises.push(renderPromise)
        }
    })

    await Promise.all(renderPromises)
}



const get_active = (): void => {
    const id = smlib.get_active()

    if (! id.music.current) {
        $(`.pdf_page`).hide()
    } else {
        $(`.pdf_page:not([data-pdf-id='${id.music.current}'])`).hide()
        $(`.pdf_page[data-pdf-id='${id.music.current}']`).show()
    }
}



const scroll_to_page = page => {
    const container = $('#pdf')
    const pages = $('.pdf_page:visible')
    const last = pages.length

    let current = parseInt(localStorage.getItem('current_pdf_page')) || 0
    if      (page === 'next'   ) { page = Math.min(last - 1, current + 1) }
    else if (page === 'prev'   ) { page = Math.max(       0, current - 1) }
    else if (page === 'current') { page = current }
    localStorage.setItem('current_pdf_page', page.toString())

    const gap = parseInt(container.css('gap')) || 0
    const position = pages
        .slice(0, page)
        .toArray()
        .reduce((total, pageElement) => {
            const pageWidth = $(pageElement).outerWidth(true)
            return total + pageWidth + gap
        }, 0)

    container.animate({ scrollLeft: position }, 100)
}



const handle_keypress = event => {
    switch (event.key) {
        case 'ArrowRight':
            event.preventDefault()
            scroll_to_page('next')
            break

        case 'ArrowLeft':
            event.preventDefault()
            scroll_to_page('prev')
            break

        default:

    }
}



const setup_events = (): void => {
    $('#manus').on('scroll', () => { get_active() })
    $('#pdf').on('click',  () => { $(document.body).toggleClass('fullscreen') })

    $(document).on('keydown',  event => handle_keypress(event) )
}



export const setup = async (): Promise<void> => {
    smlib.pdfjsLib.GlobalWorkerOptions.workerSrc = 'js/external/pdf-3.9.179.worker.min.js'

    const html: string = smlib.wrap({ tag: 'div', id: 'pdf' })
    smlib.append($(document.body), html)

    const pdf = [
        {
            "id": 2,
            "name": "Min lille fugl",
            "pdf": {
                "filename": "pdf/2 - min lille fugl.pdf",
                'pdf': null,
                'pagecount': 0,
            }
        },
        {
            "id": 3.3,
            "name": "Markedsdag",
            "pdf": {
                "filename": "pdf/3 - markedsdag.pdf",
                'pdf': null,
                'pagecount': 0,
            }
        },
        {
            "id": 5.1,
            "name": "Scene 5",
            "pdf": {
                "filename": "pdf/5 - noter.pdf",
                'pdf': null,
                'pagecount': 0,
            }
        },
        {
            "id": 7,
            "name": "Scene 7",
            "pdf": {
                "filename": "pdf/7 - noter.pdf",
                'pdf': null,
                'pagecount': 0,
            }
        },
        {
            "id": 9,
            "name": "Bakgrunnsmusikk",
            "pdf": {
                "filename": "pdf/9 - bakgrunnsmusikk.pdf",
                'pdf': null,
                'pagecount': 0,
            }
        },
        {
            "id": 13,
            "name": "Min lille fugl",
            "pdf": {
                "filename": "pdf/13 - min lille fugl.pdf",
                'pdf': null,
                'pagecount': 0,
            }
        }
    ]

    await pdf_load(pdf)
    await pdf_render(pdf)

    setup_events()
    get_active()
    scroll_to_page('current')
}
