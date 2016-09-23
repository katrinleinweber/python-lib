"""XHTML10 -- generate XHTML conformant to the 1.0 standard. See:

        http://www.w3.org/TR/xhtml1/

Implemented similarly to HTML40; see the docs in that module.

"""

__version__ = "$Revision: 1.1.1.1 $"[11:-4]

import string
from string import lower, join, replace
from sys import stdout

coreattrs = {'id': 1, 'klass': 1, 'style': 1, 'title': 1}
i18n = {'lang': 1, 'dir': 1}
intrinsic_events = {'onload': 1, 'onunload': 1, 'onclick': 1,
		    'ondblclick': 1, 'onmousedown': 1, 'onmouseup': 1,
		    'onmouseover': 1, 'onmousemove': 1, 'onmouseout': 1,
		    'onfocus': 1, 'onblur': 1, 'onkeypress': 1,
		    'onkeydown': 1, 'onkeyup': 1, 'onsubmit': 1,
		    'onreset': 1, 'onselect': 1, 'onchange': 1 }

attrs = coreattrs.copy()
attrs.update(i18n)
attrs.update(intrinsic_events)

alternate_text = {'alt': 1}
image_maps = {'shape': 1, 'coords': 1}
anchor_reference = {'href': 1}
target_frame_info = {'target': 1}
tabbing_navigation = {'tabindex': 1}
access_keys = {'accesskey': 1}

tabbing_and_access = tabbing_navigation.copy()
tabbing_and_access.update(access_keys)

visual_presentation = {'height': 1, 'width': 1, 'border': 1, 'align': 1,
		       'hspace': 1, 'vspace': 1}

cellhalign = {'align': 1, 'char': 1, 'charoff': 1}
cellvalign = {'valign': 1}

font_modifiers = {'size': 1, 'color': 1, 'face': 1}

links_and_anchors = {'href': 1, 'hreflang': 1, 'type': 1, 'rel': 1, 'rev': 1}
borders_and_rules = {'frame': 1, 'rules': 1, 'border': 1}

from SGML import Markup, Comment
from XML import XMLPI

DOCTYPE = Markup("DOCTYPE",
                 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ' \
                 '"DTD/xhtml1-transitional.dtd"')
DOCTYPE_frameset = Markup("DOCTYPE",
                 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" ' \
                 '"DTD/xhtml1-frameset.dtd"')

class Element(XMLPI):

    defaults = {}

    def __init__(self, *content, **attr):
	self.dict = {}
	if not hasattr(self, 'name'): self.name = lower(self.__class__.__name__)
	if self.defaults: self.update(self.defaults)
	self.update(attr)
	if not self.content_model and content:
	    raise TypeError, "No content for this element"
	self.content = list(content)

    def update(self, d2): 
	for k, v in d2.items(): self[k] = v

    def __setitem__(self, k, v):
	kl = lower(k)
	if self.attlist.has_key(kl): self.dict[kl] = v
	else: raise KeyError, "Invalid attribute for this element"

    start_tag_string = "<%s %s>"
    start_tag_no_attr_string = "<%s>"
    end_tag_string = "</%s>"

    def start_tag(self):
	a = self.str_attribute_list()
	return a and self.start_tag_string % (self.name, a) \
	       or self.start_tag_no_attr_string % self.name

    def end_tag(self):
	return self.end_tag_string % self.name


class PrettyTagsMixIn:

    def writeto(self, fp=stdout, indent=0, perlevel=2):
	myindent = '\n' + " "*indent
	fp.write(myindent+self.start_tag())
	for c in self.content:
	    if hasattr(c, 'writeto'):
		getattr(c, 'writeto')(fp, indent+perlevel, perlevel)
	    else:
		fp.write(str(c))
	fp.write(self.end_tag())

    def __str__(self, indent=0, perlevel=2):
	myindent = (perlevel and '\n' or '') + " "*indent
	s = [myindent, self.start_tag()]
	for c in self.content:
	    try: s.append(apply(c.__str__, (indent+perlevel, perlevel)))
	    except: s.append(str(c))
	s.append(self.end_tag())
	return join(s,'')

class CommonElement(Element): attlist = attrs

class PCElement(PrettyTagsMixIn, CommonElement): pass

class A(CommonElement):

    attlist = {'charset': 1}
    attlist.update(CommonElement.attlist)
    attlist.update(links_and_anchors)
    attlist.update(image_maps)
    attlist.update(target_frame_info)
    attlist.update(tabbing_and_access)


class ABBR(CommonElement): pass
class ACRONYM(CommonElement): pass
class CITE(CommonElement): pass
class CODE(CommonElement): pass
class DFN(CommonElement): pass
class EM(CommonElement): pass
class KBD(CommonElement): pass
class PRE(CommonElement): pass
class SAMP(CommonElement): pass
class STRONG(CommonElement): pass
class VAR(CommonElement): pass
class ADDRESS(CommonElement): pass
class B(CommonElement): pass
class BIG(CommonElement): pass
class I(CommonElement): pass
class S(CommonElement): pass
class SMALL(CommonElement): pass
class STRIKE(CommonElement): pass
class TT(CommonElement): pass
class U(CommonElement): pass
class SUB(CommonElement): pass
class SUP(CommonElement): pass
 
class DD(PCElement): pass
class DL(PCElement): pass
class DT(PCElement): pass
class NOFRAMES(PCElement): pass
class NOSCRIPTS(PCElement): pass
class P(PCElement): pass

class AREA(PCElement):

    attlist = {'nohref': 0}
    attlist.update(PCElement.attlist)
    attlist.update(image_maps)
    attlist.update(anchor_reference)
    attlist.update(tabbing_and_access)
    attlist.update(alternate_text)

class MAP(AREA): pass

class BASE(PrettyTagsMixIn, Element):

    attlist = anchor_reference.copy()
    attlist.update(target_frame_info)
    content_model = None

class BDO(Element):

    attlist = coreattrs.copy()
    attlist.update(i18n)

class BLOCKQUOTE(CommonElement):

    attlist = {'cite': 1}
    attlist.update(CommonElement.attlist)

class Q(BLOCKQUOTE): pass

class BR(PrettyTagsMixIn, Element):

    attlist = coreattrs
    content_model = None

class BUTTON(CommonElement):

    attlist = {'value': 1, 'type': 1, 'disabled': 0}
    attlist.update(CommonElement.attlist)
    attlist.update(tabbing_and_access)

class CAPTION(Element):

    attlist = {'align': 1}
    attlist.update(attrs)

class COLGROUP(PCElement):

    attlist = {'span': 1, 'width': 1}
    attlist.update(PCElement.attlist)
    attlist.update(cellhalign)
    attlist.update(cellvalign)

class COL(COLGROUP): content_model = None

class DEL(Element):

    attlist = {'cite': 1, 'datetime': 1}
    attlist.update(attrs)

class INS(DEL): pass

class FIELDSET(PCElement): pass

class LEGEND(PCElement):
    
    attlist = {'align': 1}
    attlist.update(PCElement.attlist)
    attlist.update(access_keys)

class BASEFONT(Element):

    attlist = {'id': 1}
    attlist.update(font_modifiers)
    content_model = None

class FONT(Element):

    attlist = font_modifiers.copy()
    attlist.update(coreattrs)
    attlist.update(i18n)

class FORM(PCElement):

    attlist = {'action': 1, 'method': 1, 'enctype': 1, 'accept_charset': 1,
	       'target': 1}
    attlist.update(PCElement.attlist)

class FRAME(PrettyTagsMixIn, Element):

    attlist = {'longdesc': 1, 'src': 1, 'frameborder': 1,
	       'marginwidth': 1, 'marginheight': 1, 'noresize': 0,
	       'scrolling': 1}
    attlist.update(coreattrs)
    content_model = None

class FRAMESET(PrettyTagsMixIn, Element):

    attlist = {'rows': 1, 'cols': 1, 'border': 1}
    attlist.update(coreattrs)
    attlist.update(intrinsic_events)

class Heading(PCElement):

    attlist = {'align': 1}
    attlist.update(attrs)

    def __init__(self, level, *content, **attr):
	self.level = level
	apply(PCElement.__init__, (self,)+content, attr)

    def start_tag(self):
	a = self.str_attribute_list()
	return a and "<H%d %s>" % (self.level, a) or "<H%d>" % self.level

    def end_tag(self):
	return self.content_model and "</H%d>\n" % self.level or ''

class HEAD(PrettyTagsMixIn, Element):

    attlist = {'profile': 1}
    attlist.update(i18n)

class HR(Element):

    attlist = {'align': 1, 'noshade': 0, 'size': 1, 'width': 1}
    attlist.update(coreattrs)
    attlist.update(intrinsic_events)
    content_model = None

class HTML(PrettyTagsMixIn, Element):

    attlist = i18n

class TITLE(HTML): pass

class BODY(PCElement):

    attlist = {'background': 1, 'text': 1, 'link': 1, 'vlink': 1, 'alink': 1,
	       'bgcolor': 1}
    attlist.update(PCElement.attlist)

class IFRAME(PrettyTagsMixIn, Element):

    attlist = {'longdesc': 1, 'src': 1, 'frameborder': 1,
	       'marginwidth': 1, 'marginheight': 1, 'scrolling': 1, 
	       'align': 1, 'height': 1, 'width': 1}
    attlist.update(coreattrs)

class IMG(CommonElement):

    attlist = {'src': 1, 'longdesc': 1, 'usemap': 1, 'ismap': 0}
    attlist.update(PCElement.attlist)
    attlist.update(visual_presentation)
    attlist.update(alternate_text)
    content_model = None

class INPUT(CommonElement):

    attlist = {'type': 1, 'value': 1, 'checked': 0, 'disabled': 0,
	       'readonly': 0, 'size': 1, 'maxlength': 1, 'src': 1,
	       'usemap': 1, 'accept': 1, 'border': 1}
    attlist.update(CommonElement.attlist)
    attlist.update(tabbing_and_access)
    attlist.update(alternate_text)
    content_model = None

class LABEL(CommonElement):

    attlist = {'label_for': 1}
    attlist.update(CommonElement.attlist)
    attlist.update(access_keys)

class UL(PCElement):
    
    attlist = {'compact': 0}
    attlist.update(CommonElement.attlist)

class OL(UL):

    attlist = {'start': 1}
    attlist.update(UL.attlist)

class LI(UL):

    attlist = {'value': 1, 'type': 1}
    attlist.update(UL.attlist)

class LINK(PCElement):

    attlist = {'charset': 1, 'media': 1}
    attlist.update(PCElement.attlist)
    attlist.update(links_and_anchors)
    content_model = None

class META(PrettyTagsMixIn, Element):

    attlist = {'http_equiv': 1, 'content': 1, 'scheme': 1}
    attlist.update(i18n)
    content_model = None

class OBJECT(PCElement):

    attlist = {'declare': 0, 'classid': 1, 'codebase': 1, 'data': 1,
	       'type': 1, 'codetype': 1, 'archive': 1, 'standby': 1,
	       'height': 1, 'width': 1, 'usemap': 1}
    attlist.update(PCElement.attlist)
    attlist.update(tabbing_navigation)

class SELECT(PCElement):

    attlist = {'size': 1, 'multiple': 0, 'disabled': 0}
    attlist.update(CommonElement.attlist)
    attlist.update(tabbing_navigation)

class OPTGROUP(PCElement):

    attlist = {'disabled': 0, 'label': 1}
    attlist.update(CommonElement.attlist)

class OPTION(OPTGROUP):

    attlist = {'value': 1, 'selected': 0}
    attlist.update(OPTGROUP.attlist)

class PARAM(Element):

    attlist = {'id': 1, 'value': 1, 'valuetype': 1, 'type': 1}

class SCRIPT(Element):

    attlist = {'charset': 1, 'type': 1, 'src': 1, 'defer': 0}

class SPAN(CommonElement):

    attlist = {'align': 1}
    attlist.update(CommonElement.attlist)

class DIV(PrettyTagsMixIn, SPAN): pass

class STYLE(PrettyTagsMixIn, Element):

    attlist = {'type': 1, 'media': 1, 'title': 1}
    attlist.update(i18n)

class TABLE(PCElement):

    attlist = {'cellspacing': 1, 'cellpadding': 1, 'summary': 1, 'align': 1,
	       'bgcolor': 1, 'width': 1}
    attlist.update(CommonElement.attlist)
    attlist.update(borders_and_rules)

class TBODY(PCElement):

    attlist = CommonElement.attlist.copy()
    attlist.update(cellhalign)
    attlist.update(cellvalign)

class THEAD(TBODY): pass
class TFOOT(TBODY): pass
class TR(TBODY): pass

class TH(TBODY):

    attlist = {'abbv': 1, 'axis': 1, 'headers': 1, 'scope': 1,
	       'rowspan': 1, 'colspan': 1, 'nowrap': 0, 'width': 1, 
	       'height': 1}
    attlist.update(TBODY.attlist)

class TD(TH): pass

class TEXTAREA(CommonElement):

    attlist = {'rows': 1, 'cols': 1, 'disabled': 0, 'readonly': 0}
    attlist.update(CommonElement.attlist)
    attlist.update(tabbing_and_access)

def CENTER(*content, **attr):
    c = apply(DIV, content, attr)
    c['align'] = 'center'
    return c

def H1(content=[], **attr): return apply(Heading, (1, content), attr)
def H2(content=[], **attr): return apply(Heading, (2, content), attr)
def H3(content=[], **attr): return apply(Heading, (3, content), attr)
def H4(content=[], **attr): return apply(Heading, (4, content), attr)
def H5(content=[], **attr): return apply(Heading, (5, content), attr)
def H6(content=[], **attr): return apply(Heading, (6, content), attr)

class CSSRule(PrettyTagsMixIn, Element):

    attlist = {'font': 1, 'font_family': 1, 'font_face': 1, 'font_size': 1,
	       'border': 1, 'border_width': 1, 'color': 1,
	       'background': 1, 'background_color': 1, 'background_image': 1,
	       'text_align': 1, 'text_decoration': 1, 'text_indent': 1,
	       'line_height': 1, 'margin_left': 1, 'margin_right': 1,
	       'clear': 1, 'list_style_type': 1}
    content = []
    content_model = None

    def __init__(self, selector, **decl):
	self.dict = {}
	self.update(decl)
	self.name = selector

    start_tag_string = "%s { %s }"

    def end_tag(self): return ''

    def str_attribute(self, k):
	kt = replace(k, '_', '-')
	if self.attlist[k]: return '%s: %s' % (kt, str(self[k]))
	else: return self[k] and kt or ''

    def str_attribute_list(self):
	return join(map(self.str_attribute, self.dict.keys()), '; ')

nbsp = "&nbsp;"

def quote_body(s):
    r=replace; return r(r(r(s, '&', '&amp;'), '<', '&lt;'), '>', '&gt;')

safe = string.letters + string.digits + '_,.-'

def url_encode(s):
    l = []
    for c in s:
	if c in safe:  l.append(c)
	elif c == ' ': l.append('+')
	else:          l.append("%%%02x" % ord(c))
    return join(l, '')

def URL(*args, **kwargs):
    url_path = join(args, '/')
    a = []
    for k, v in kwargs.items():
	a.append("%s=%s" % (url_encode(k), url_encode(v)))
    url_vals = join(a, '&')
    return url_vals and join([url_path, url_vals],'?') or url_path

def Options(options, selected=[], **attrs):
    opts = []
    for o, v in options:
	opt = apply(OPTION, (o,), attrs)
	opt['value'] = v
	if v in selected: opt['selected'] = 1
	opts.append(opt)
    return opts

def Select(options, selected=[], **attrs):
    return apply(SELECT, tuple(apply(Options, (options, selected))), attrs)

def Href(url, text, **attrs):
    h = apply(A, (text,), attrs)
    h['href'] = url
    return h

def Mailto(address, text, subject='', **attrs):
    if subject:
	url = "mailto:%s?subject=%s" % (address, subject)
    else:
	url = "mailto:%s" % address
    return apply(Href, (url, text), attrs)

def Image(src, **attrs):
    i = apply(IMG, (), a)
    i['src'] = src
    return i

def StyledTR(element, row, klasses):
    r = TR()
    for i in range(len(row)):
	r.append(klasses[i] and element(row[i], klass=klasses[i]) \
			    or  element(row[i]))
    return r

def StyledVTable(klasses, *rows, **attrs):
    t = apply(TABLE, (), attrs)
    t.append(COL(span=len(klasses)))
    for row in rows:
	r = StyledTR(TD, row[1:], klasses[1:])
	h = klasses[0] and TH(row[0], klass=klasses[0]) \
	               or  TH(row[0])
	r.content.insert(0,h)
	t.append(r)
    return t

def VTable(*rows, **attrs):
    t = apply(TABLE, (), attrs)
    t.append(COL(span=len(rows[0])))
    for row in rows:
	r = apply(TR, tuple(map(TD, row[1:])))
	r.content.insert(0, TH(row[0]))
	t.append(r)
    return t

def StyledHTable(klasses, headers, *rows, **attrs):
    t = apply(TABLE, (), attrs)
    t.append(COL(span=len(headers)))
    t.append(StyledTR(TH, headers, klasses))
    for row in rows: t.append(StyledTR(TD, row, klasses))
    return t

def HTable(headers, *rows, **attrs):
    t = apply(TABLE, (), attrs)
    t.append(COL(span=len(headers)))
    t.append(TR, tuple(map(TH, headers)))
    for row in rows: t.append(TR(apply(TD, row)))
    return t

def DefinitionList(*items, **attrs):
    dl = apply(DL, (), attrs)
    for dt, dd in items: dl.append(DT(dt), DD(dd))
    return dl


