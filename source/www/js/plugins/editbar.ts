import { smlib } from '../modules/smlib.js'
import { data  } from '../modules/data.js'



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



const create_draggable = (): void => {
    let $placeholder; // Placeholder for sorting
    let $clonedItem; // Clone of the dragged item
    let inSortable = false; // Flag to track if we're in a sortable container

    // Make cues in #editbar draggable
    $('#editbar .cue').draggable({
        helper: 'clone', // Clone the dragged element
        revert: 'invalid', // Revert back if not dropped in a valid area
        cursor: 'move',
        zIndex: 100,
        start: function (event, ui) {
            console.log('Drag started');
            inSortable = false; // Reset the flag on start
        },
        drag: function (event, ui) {
            // Get the Y position of the draggable
            const draggableY = ui.helper.offset().top + ui.helper.outerHeight() / 2;

            // Find the scene under the draggable
            const targetScene = $('#manus .scene').filter(function () {
                const offset = $(this).offset();
                const height = $(this).outerHeight();
                return draggableY >= offset.top && draggableY <= offset.top + height;
            }).first();

            if (targetScene.length) {
                // Ensure we have a placeholder and a clone
                if (!$placeholder) {
                    $placeholder = $('<div class="cues-placeholder"></div>').height(40); // Match height
                }
                if (!$clonedItem) {
                    $clonedItem = $(ui.helper).clone().addClass('cues'); // Clone the draggable
                }

                // Flag that we're now interacting with a sortable
                inSortable = true;

                // Append the placeholder if not already in the scene
                if (!targetScene.find($placeholder).length) {
                    targetScene.append($placeholder);
                }

                // Position the placeholder dynamically
                targetScene.children('.cues, .cues-placeholder').each(function () {
                    const itemY = $(this).offset().top + $(this).outerHeight() / 2;
                    if (draggableY < itemY) {
                        $placeholder.insertBefore(this);
                        return false; // Break out of the loop
                    }
                });
            } else {
                inSortable = false; // Not hovering over a sortable
                if ($placeholder) $placeholder.detach(); // Remove placeholder if not in a sortable
            }
        },
        stop: function (event, ui) {
            console.log('Drag stopped');

            if (inSortable && $placeholder) {
                // Insert the cloned item at the placeholder's position
                $clonedItem.insertBefore($placeholder);
                $placeholder.remove();
                $placeholder = null;

                // Refresh sortable to recognize the new item
                $clonedItem.closest('.scene').sortable('refresh');

                // Update data
                update_data($clonedItem);

                $clonedItem = null; // Clear the clone
            } else {
                // Cleanup if drag is aborted
                if ($placeholder) $placeholder.remove();
                $placeholder = null;
                $clonedItem = null;
            }
        }
    });

    // Make scenes sortable
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

    $('.scene').disableSelection()}



const setup_events = (): void => {
    create_draggable()
}



export const setup = async (): Promise<void> => {
    const contents: string[] = [
        smlib.wrap({ tag: 'div', classes: ['cue', 'music', 'start'], contents: ['music start'] })
    ]

    const html: string = smlib.wrap({ tag: 'div', id: 'editbar', contents: contents })
    smlib.append($(document.body), html)

    setup_events()
}
