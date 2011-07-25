
from jpath.query import syntax
from pango import FontDescription

tail = ["string or embedded literal", "string", "identifier with dot",
        "identifier without dot",
        "alpha identifier with dot", "alpha identifier without dot", 
        "number", "alphanum", "alpha", "digit", "upper", "lower"]

if __name__ == "__main__":
    print "Enter a .png filename where syntax diagrams will be written to"
    name = raw_input()
    if not name[-4:] == ".png":
        raise Exception("That doesn't end with .png")
    """
        raildraw_production_font=bold_font,
        raildraw_text_font=bold_font,
        raildraw_anycase_font=plain_font,
        raildraw_description_font=plain_font,
    """
    plain_font = FontDescription("sans 9")
    bold_font = FontDescription("sans bold 9")
    italic_font = FontDescription("sans italic 9")
    title_font = FontDescription("sans bold 12")
    syntax.module.draw_productions_to_png({ #@UndefinedVariable
            "raildraw_production_font": plain_font,
            "raildraw_text_font": bold_font,
            "raildraw_anycase_font": plain_font,
            "raildraw_description_font": italic_font,
            "raildraw_title_font": title_font,
            "raildraw_arrow_width": 8,
            "raildraw_arrow_height": 7,
            "raildraw_line_size": 1.5,
            "raildraw_title_after": 40
            }, name, tail=tail)
    print "done"
    