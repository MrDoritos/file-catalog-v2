class CatalogItem {
    id;
    name; 
    parents;
    children;
    x;
    y;
}

class Index {
    catalog = []
    async getItemById(id) {
        return await this.getItem({id: id});
    }
    async getItemByName(name) {
        return await this.getItem({name: name});
    }
    async getItem(item) {
        return await this.updateItem(
            await API.post('/api/index/getItem', item));
        
    }
    async getFirstOrderItems() {
        return await this.updateItems(
            await API.get('/api/index/getFirstOrderItems'));
        
    }
    async getItems() {
        return await this.updateItems(
            await API.get('/api/index/getItems'));
    }
    async updateItem(item) {
        if (item) {
            console.log('Adding item: ', item);
            this.catalog[item.id] = item;
            indexof = this.catalog.findIndex(item => item.id == item.id);
            if (indexof != -1) {
                this.catalog[indexof] = item;
            } else {
                this.catalog.push(item);
            }
        }
        return item;
    }
    async updateItems(items) {
        console.log('Adding items: ', items);
        if (items) {
            items.forEach(item => {
                console.log('Adding item: ', item);
                this.updateItem(item);
            });
        }
        return items;
    }
    async getParentItems(item) {
        return await this.updateItems(
            await API.post('/api/index/getParentItems', item));
    }
    async getChildItems(item) {
        return await this.updateItems(
            await API.post('/api/index/getChildItems', item));
    }
    async addItem(name) {
        return await this.updateItem(
            await API.post('/api/index/addItem', {name: name}));
    }
    async modifyItem(item) {
        return await this.updateItem(
            await API.post('/api/index/modifyItem', item));
    }
    async addOrGetItem(name) {
        return await this.updateItem(
            await API.post('/api/index/addOrGetItem', {name: name}));
    }
    async getVector(name) {
        vec = await API.post('/api/index/getVector', {name: name});
        return vec.x, vec.y;
    }
    async calculateVector(item) {
        vec = await API.post('/api/index/calculateVector', item);
        item.x = vec.x;
        item.y = vec.y;
        return vec.x, vec.y;
    }
}

class API {
    static BASE_URL = "http://localhost:8000";
    static async use_response(response) {
        console.log('Response:', await response);
        json = await response.json();
        if (data.item)
            return data.item;
        if (data.items)
            return data.items;
        return null;
    }
    static async get(url) {
        try {
            var response = await fetch(this.BASE_URL + url);
            return await this.use_response(response);
        } catch (error) {
            console.error(error);
        }
        return null;
    }
    static async post(url, item) {
        try {
            var response = await fetch(this.BASE_URL + url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(item)
            });
            return await this.use_response(response);
        } catch (error) {
            console.error(error);
        }
        return null;
    }
}