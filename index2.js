// Get the canvas element and its context
const canvas = document.getElementById('canvasVectorSpace');
const canvasSelectedItem = document.getElementById('canvasSelectedItem');
const ctx = canvas.getContext('2d');
const ctxSelectedItem = canvasSelectedItem.getContext('2d');
//var CatalogItems = []; // Array to store all items
var SelectedItem = null; // Variable to store the selected item
var index = new Index();
// Fetch all items from the API
function getCatalogFirstOrderItems() {
    return index.getFirstOrderItems();
}

function getChildItems(id) {
    return index.getChildItems({id:id});
}

function getCatalogItems() {
    return index.getItems();
}

var scalingFactor = 1.1;
var zoomFactor = 1;
var canvasPositionX = 0.5;
var canvasPositionY = 0.5;

function convertToCanvasX(x) {
    return (x + ((canvas.width / scalingFactor) * 0.5) + canvasPositionX) * scalingFactor;
    //return (x + 0.5 + canvasPositionX) * scalingFactor;
}

function convertToCanvasY(y) {
    return (y + ((canvas.height / scalingFactor) * 0.5) + canvasPositionY) * scalingFactor;
    //return (y + 0.5 + canvasPositionY) * scalingFactor;
}

let isDragging = false;
let singleClick = false;
let lastMouseX = 0;
let lastMouseY = 0;

canvas.addEventListener('wheel', function(event) {
    event.preventDefault();
    const delta = Math.sign(event.deltaY);
    const zoomStep = 0.1;
    if (delta > 0) {
        zoomFactor -= zoomStep;
    } else {
        zoomFactor += zoomStep;
    }
    //console.log("Delta: " + delta +
    // " canvasPositionX: " + canvasPositionX + " canvasPositionY: " + canvasPositionY + " zoomFactor: " + zoomFactor + " scalingFactor: " + scalingFactor);
    // Adjust the canvas position to center the zooming

    zoomCanvas(zoomFactor);
});

canvas.addEventListener('mousemove', function(event) {
    if (isDragging) {
        singleClick = false;
        const deltaX = event.clientX - lastMouseX;
        const deltaY = event.clientY - lastMouseY;
        canvasPositionX += (deltaX / scalingFactor);
        canvasPositionY += (deltaY / scalingFactor);
        lastMouseX = event.clientX;
        lastMouseY = event.clientY;
        drawCatalogItems();
    }
});

canvas.addEventListener('mouseleave', function(event) {
    isDragging = false;
});
//canvas.addEventListener('mouseup', function(event) {
//    isDragging = false;
//});

canvas.addEventListener('mousedown', function(event) {
    isDragging = true;
    singleClick = true;
    lastMouseX = event.clientX;
    lastMouseY = event.clientY;
});

function setVisibility(item, visible, depth=0, maxdepth=5) {
    item.visible = visible;
    if (depth == 0) {
        index.catalog.forEach(item2 => {
            item2.items.forEach(subItem => {
                if (item.id == subItem)
                    item2.visible = true;
            });
        });
    }
    if (item.items.length > 0 && depth < maxdepth) {
        item.items.forEach(subItem => {
            const subItem2 = index.catalog.find(item => item.id == subItem);
            setVisibility(subItem2, visible, depth+1, maxdepth);
        });
    }
}

canvas.addEventListener('mouseup', function(event) {
    isDragging = false;

    if (!singleClick)
        return;

    // Get the mouse coordinates relative to the canvas
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    // Loop through each item and check if the mouse coordinates are within its bounds
    //CatalogItems.forEach((item, index) => {

    index.catalog.forEach(item => {
        item.visible = true;
    });

    for (var i = 0; i < index.catalog.length; i++) {
        var item = index.catalog[i];
        // Calculate the bounds of the item
        const itemX = convertToCanvasX(item.x);
        const itemY = convertToCanvasY(item.y);
        const itemWidth = ctx.measureText(item.name).width;
        const itemHeight = 20;

        // Check if the mouse coordinates are within the bounds of the item
        if (mouseX >= itemX && mouseX <= itemX + itemWidth && mouseY >= itemY && mouseY <= itemY + itemHeight) {
            // Item is selected, do something with it
            console.log('Selected item:', item);
            index.catalog.forEach(item => {
                item.visible = false;
            });
            setVisibility(item, true);
            /*
            for (var i = 0; i < CatalogItems.length; i++) {
                CatalogItems[i].visible = false;
                CatalogItems[i].items.forEach(subItem => {
                    if (item.id == subItem) {
                        CatalogItems[i].visible = true;
                    }                
                });
                if (CatalogItems[i].id == item.id) {
                    CatalogItems[i].visible = true;
                }
                item.items.forEach(subItem => {
                    if (CatalogItems[i].id == subItem) {
                        CatalogItems[i].visible = true;
                    }
                });
            }*/
            setSelectedItem(item);
            break;
        } 

    }

    drawCatalogItems();
});

function get_catalog_item(id) {
    return index.getItem({id:id});
}

function get_catalog_name_vectors() {
    const nameVectors = {};
    index.catalog.forEach(item => {
        if (item.items.length > 0)
            return;
        //const { name, x, y } = CatalogItems.find(item2 => item2.id == item.items[0]);
        index.catalog.forEach(item2 => {
            if (item.id != item2.items[0])
                return;

            const name = item.name;
            const x = item2.x;
            const y = item2.y;

            if (!nameVectors[name]) {
                nameVectors[name] = {
                    minX: x,
                    minY: y,
                    maxX: x,
                    maxY: y
                };
            } else {
                const vector = nameVectors[name];
                vector.minX = Math.min(vector.minX, x);
                vector.minY = Math.min(vector.minY, y);
                vector.maxX = Math.max(vector.maxX, x);
                vector.maxY = Math.max(vector.maxY, y);
            }
        });        
    });
    return nameVectors;
}

function drawSelectedItem() {
    if (SelectedItem) {
        // Clear the ctxSelectedItem canvas
        ctxSelectedItem.clearRect(0, 0, canvasSelectedItem.width, canvasSelectedItem.height);
        
        // Draw the selected item on ctxSelectedItem
        const selectedItemX = convertToCanvasX(SelectedItem.x);
        const selectedItemY = convertToCanvasY(SelectedItem.y);
        const selectedItemWidth = ctx.measureText(SelectedItem.name).width;
        const selectedItemHeight = 20;
        
        ctxSelectedItem.fillStyle = 'yellow';
        ctxSelectedItem.fillRect(selectedItemX, selectedItemY, selectedItemWidth, selectedItemHeight);
        
        // Draw child items
        SelectedItem.items.forEach(childItemId => {
            const childItem = index.catalog.find(item => item.id === childItemId);
            if (childItem) {
                const childItemX = convertToCanvasX(childItem.x);
                const childItemY = convertToCanvasY(childItem.y);
                const childItemWidth = ctx.measureText(childItem.name).width;
                const childItemHeight = 20;
                
                ctxSelectedItem.fillStyle = 'green';
                ctxSelectedItem.fillRect(childItemX, childItemY, childItemWidth, childItemHeight);
            }
        });
    }
}

function drawCatalogItems() {
    autoscaleItems(); // Autoscale the items

    ctx.clearRect(-canvas.width, -canvas.height, canvas.width * 2, canvas.height * 2); // Clear the canvas

    //ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform
    //ctx.translate(canvasPositionX + canvas.width / 2, canvasPositionY + canvas.height / 2); // Pan
    //ctx.scale(zoomFactor, zoomFactor); // Zoom
    //ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    index.catalog.forEach((item, index) => {
        // Calculate the coordinates of the selectable area
        const itemX = convertToCanvasX(item.x);
        const itemY = convertToCanvasY(item.y);
        if (itemX > -1 && itemX < canvas.width && itemY > -1 && itemY < canvas.height && item.visible) {
            const itemWidth = ctx.measureText(item.name).width;
            const itemHeight = 20;
            
            // Draw a circle around the selectable area
            ctx.beginPath();
            ctx.arc(itemX + itemHeight / 2, itemY + itemHeight / 2, itemHeight / 2, 0, 2 * Math.PI);
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Add text of the data inside the selectable area
            ctx.fillText(item.name, itemX, itemY);
            //ctx.fillText(item.name, itemX, itemY + itemHeight);
        }
    });


    const nameVectors = get_catalog_name_vectors();
    Object.keys(nameVectors).forEach(name => {
        const vector = nameVectors[name];
        const centerX = (vector.minX);
        const centerY = (vector.minY);
        const itemX = convertToCanvasX(centerX);
        const itemY = convertToCanvasY(centerY);
        const itemHeight = convertToCanvasY(vector.maxY) - convertToCanvasY(vector.minY);
        
        // Draw a circle around the selectable area
        ctx.beginPath();
        ctx.arc(itemX + itemHeight / 2, itemY + itemHeight / 2, itemHeight / 2, 0, 2 * Math.PI);
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Add text of the name inside the selectable area
        ctx.fillText(name, itemX, itemY + itemHeight);
    });

}

function zoomCanvas(scale) {
    //console.log(scale);
    // Update the scaling factor
    zoomFactor = scale;
    
    // Adjust the canvas position to center the zooming

    // Redraw the catalog items with the new scaling factor
    drawCatalogItems();
}
// Autoscale all items on the canvas using a scaling factor
function autoscaleItems() {
    // Determine a global scaling factor here
    const minX = Math.min(...index.catalog.map(item => item.x));
    const maxX = Math.max(...index.catalog.map(item => item.x));
    const minY = Math.min(...index.catalog.map(item => item.y));
    const maxY = Math.max(...index.catalog.map(item => item.y));
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    const scaleX = canvasWidth / (maxX - minX);
    const scaleY = canvasHeight / (maxY - minY);
    scalingFactor = Math.min(scaleX, scaleY) * zoomFactor;
    //console.log("scalingFactor: " + scalingFactor);
}


//getCatalogItems();
getCatalogFirstOrderItems();
drawCatalogItems();

autoscaleItems();

function set_catalog_item(item) {
    return index.modifyItem(item);
}

function add_catalog_item(name) {
    return index.addItem(name);
}

function addItem() {
    // Create a new item object
    const form = document.getElementById('addItem');
    const nameInput = form.querySelector('input[name="name"]');
    //const dataInput = form.querySelector('input[name="data"]');

    console.log(add_catalog_item(nameInput.value));
}

function setSelectedItem(item) {
    SelectedItem = item;
    console.log("Set selected item");
    getChildItems(SelectedItem.id);
    drawSelectedItem();
    return;
    const form = document.getElementById('editItem');
    //const idInput = form.querySelector('input[name="id"]');
    const nameInput = form.getElementById('name');
    const dataInput = form.querySelector('input[id="data"]');
    const xInput = form.querySelector('input[id="x"]');
    const yInput = form.querySelector('input[id="y"]');
    
    // Populate the fields with the selected item's data
    //idInput.value = item.id;
    nameInput.value = item.name;
    dataInput.value = item.data;
    xInput.value = item.x;
    yInput.value = item.y;
}

function editItem() {
    // Get the form inputs
    const form = document.getElementById('editItem');
    const idInput = form.querySelector('input[name="id"]');
    const nameInput = form.querySelector('input[name="name"]');
    const dataInput = form.querySelector('input[name="data"]');
    const xInput = form.querySelector('input[name="x"]');
    const yInput = form.querySelector('input[name="y"]');
    const childInput = form.querySelector('input[name="subItemId"]');
    
    // Create a new item object
    const editedItem = {
        name: nameInput.value
    };
    
    // Call the set_catalog_item function to update the item
    set_catalog_item(editedItem);
}