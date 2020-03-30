def british_trees_dict():
    """
    Return dictionary of native trees in Britain
    (key: binomial name; value: vernacular name in UK).
    Source: https://www.woodlandtrust.org.uk/trees-woods-and-wildlife/british-trees/native-trees/
    """
    tree_dict = {
        "native":{    
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
        },
        "non_native":{
            "Malus x domestica": "apple",
            "Fagus sylvatica f. purpurea": "copper beech",
            "Cedrus libani": "cedar",
            "Prunus cerasifera": "cherry plum",
            "Prunus cerasus": "sour cherry",
            "Ulmus minor": "field elm",
            "Aesculus hippocastanum": "horse chestnut",
            "Castanea sativa": "sweet chestnut",
            "Cupressus x leylandii": "Leyland cypress",
            "Chamaecyparis lawsoniana": "Lawson cypress",
            "Ulmus x hollandica 'vegeta'": "Huntingdon elm",
            "Eucalyptus spp.": "eucalyptus",
            "Pseudotsuga menziesii": "Douglas fir",
            "Tsuga heterophylla": "western hemlock",
            "Larix decidua": "European larch",
            "Acer platanoides": "Norway maple",
            "Araucaria araucana": "monkey puzzle",
            "Quercus ilex": "holm oak",
            "Quercus rubra": "red oak",
            "Quercus cerris": "Turkey oak",
            "Pyrus communis": "pear",
            "Pinus nigra": "black pine",
            "Platanus x hispanica": "London plane",
            "Prunus domestica": "plum",
            "Populus alba": "white poplar",
            "Picea abies": "Norway spruce",
            "Picea sitchensis": "Sitka spruce",
            "Acer pseudoplatanus": "sycamore",
            "Juglans regia": "walnut",
            "Juglans nigra": "black walnut",
            "Thuja plicata": "Western red cedar",
            "Taxus baccata 'fastigiata'":"Irish yew"
        }
    }
    return tree_dict


def native_trees_list():
    """
    Get list from dictionay in native_trees_dict(),
    so that it can be used to request the speciesKey in GBIF.
    """
    native_tree_dict = british_trees_dict()["native"]
    return list(native_tree_dict.keys())


if __name__ == "__main__":
    print(native_trees_list())
    assert len(native_trees_list()) == 46, "Incorrect number of native trees"