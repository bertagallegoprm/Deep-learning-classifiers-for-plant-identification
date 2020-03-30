def native_trees_dict():
    """
    Return dictionary of native trees in Britain
    (key: binomial name; value: vernacular name in UK).
    Source: https://www.woodlandtrust.org.uk/trees-woods-and-wildlife/british-trees/native-trees/
    """
    tree_dict = {
        "Alnus glutinosa": "alder",
        "Frangula alnus": "alder buckthorn",
        "Fraxinus excelsior": "ash",
        "Populus tremula": "aspen",
        "Fagus sylbatica": "common beech",
        "Betula pubescens": "downy birch",
        "Betula pendula": "silver birch", 
        "Prunus spinosa": "blackthorn",
        "Buxus sempervirens": "common box",
        "Rhamnus cathartica": "purging buckthorn",
        "Prunus padus": "bird cherry",
        "Prunus avium": "wild cherry",
        "Malus sylvestris": "crab apple",
        "Cornus sanguinea": "dogwood",
        "Sambucus nigra": "elder",
        "Ulmus procera": "English elm",
        "Ulmus glabra": "wych elm",
        "Viburnum opulus": "guelder rose",
        "Crataegus monogyna": "hawthorn",
        "Crataegus laevigata": "Midland hawthorn",
        "Corylus avellana": "hazel",
        "Ilex aquifolium": "holly",
        "Carpinus betulus": "hornbeam",
        "Juniperus communis": "juniper",
        "Tilia x europaea": "common lime", 
        "Tilia platyphyllos": "large-leaved lime",
        "Tilia cordata": "small-leaved lime",
        "Acer campestre": "field maple",
        "Quercus robur": "English oak",
        "Quercus petraea": "sessile oak",
        "Pyrus cordata": "Plymouth pear",
        "Pinus sylvestris": "Scots pine", 
        "Populus nigra": "black poplar", 
        "Sorbus aucuparia": "rowan", 
        "Euonymus europaea": "spindle",
        "Sorbus aria": "whitebeam", 
        "Sorbus arranensis": "Arran whitebeam",
        "Sorbus rupicola": "rock whitebeam",
        "Sorbus torminalis": "wild service tree",
        "Salix pentandra": "bay willow",
        "Salix fragilis": "crack willow",
        "Salix caprea": "goat willow",
        "Salix cinerea subsp. oleifolia": "grey willow",
        "Salix viminalis": "osier willow",
        "Salix alba": "white willow",
        "Taxus baccata": "yew"
    }
    return tree_dict


def native_trees_list():
    """
    Get list from dictionay in native_trees_dict(),
    so that it can be used to request the speciesKey in GBIF.
    """
    tree_dict = native_trees_dict()
    return list(tree_dict.keys())


if __name__ == "__main__":
    print(native_trees_list())
    assert len(native_trees_list()) == 46, "Incorrect number of native trees"