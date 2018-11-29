var componentList = [];

class ComponentListModel {
    static setComponentList(list) {
        componentList = list;
    }

    static getComponentList() {
        return componentList;
    }
}


export {
    ComponentListModel
};