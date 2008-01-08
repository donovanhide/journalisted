#!/usr/bin/env python2.4
#
# Copyright (c) 2007 Media Standards Trust
# Licensed under the Affero General Public License
# (http://www.affero.org/oagpl.html)

import getopt
import re
from datetime import datetime
from optparse import OptionParser
import sys

sys.path.append("../pylib")
from BeautifulSoup import BeautifulSoup
from JL import ArticleDB,ukmedia


# sources used by FindArticles
# (generated by ../hacks/indy-scrape-rsslist.py)
rssfeeds = {
	'  Home': 'http://www.independent.co.uk/index.jsp?service=rss',
	'    News': 'http://news.independent.co.uk/index.jsp?service=rss',
	'      Health': 'http://news.independent.co.uk/health/index.jsp?service=rss',
	'      Sci_Tech': 'http://news.independent.co.uk/sci_tech/index.jsp?service=rss',
	'      Robert Fisk': 'http://news.independent.co.uk/fisk/index.jsp?service=rss',
	'      UK': 'http://news.independent.co.uk/uk/index.jsp?service=rss',
	'        Crime': 'http://news.independent.co.uk/uk/crime/index.jsp?service=rss',
	'        Legal': 'http://news.independent.co.uk/uk/legal/index.jsp?service=rss',
	'        UK Politics': 'http://news.independent.co.uk/uk/politics/index.jsp?service=rss',
	'        This Britain': 'http://news.independent.co.uk/uk/this_britain/index.jsp?service=rss',
	'        Transport': 'http://news.independent.co.uk/uk/transport/index.jsp?service=rss',
	'        Ulster': 'http://news.independent.co.uk/uk/ulster/index.jsp?service=rss',
	'      Europe': 'http://news.independent.co.uk/europe/index.jsp?service=rss',
	'      World': 'http://news.independent.co.uk/world/index.jsp?service=rss',
	'        World Politics': 'http://news.independent.co.uk/world/politics/index.jsp?service=rss',
	'        Africa': 'http://news.independent.co.uk/world/africa/index.jsp?service=rss',
	'        Americas': 'http://news.independent.co.uk/world/americas/index.jsp?service=rss',
	'        Asia': 'http://news.independent.co.uk/world/asia/index.jsp?service=rss',
	'        Australasia': 'http://news.independent.co.uk/world/australasia/index.jsp?service=rss',
	'        Middle East': 'http://news.independent.co.uk/world/middle_east/index.jsp?service=rss',
	'      Business': 'http://news.independent.co.uk/business/index.jsp?service=rss',
	'        Business News': 'http://news.independent.co.uk/business/news/index.jsp?service=rss',
	'        Business Analysis & Features': 'http://news.independent.co.uk/business/analysis_and_features/index.jsp?service=rss',
	'        Business Comment': 'http://news.independent.co.uk/business/comment/index.jsp?service=rss',
	'        SME': 'http://news.independent.co.uk/business/sme/index.jsp?service=rss',
	'      Media': 'http://news.independent.co.uk/media/index.jsp?service=rss',
	'      People': 'http://news.independent.co.uk/people/index.jsp?service=rss',
	'        Obituaries': 'http://news.independent.co.uk/people/obituaries/index.jsp?service=rss',
	'        Profiles': 'http://news.independent.co.uk/people/profiles/index.jsp?service=rss',
	'        Pandora': 'http://news.independent.co.uk/people/pandora/index.jsp?service=rss',
	'      Appeals': 'http://news.independent.co.uk/appeals/index.jsp?service=rss',
	'        Indy Appeal': 'http://news.independent.co.uk/appeals/indy_appeal/index.jsp?service=rss',
	'        IoS Appeal': 'http://news.independent.co.uk/appeals/ios_appeal/index.jsp?service=rss',
			# irrelevant?
#	'      P1 images': 'http://news.independent.co.uk/p1images/index.jsp?service=rss', #BUSTED(404)

	'      Corrections': 'http://news.independent.co.uk/corrections/index.jsp?service=rss',
	'    Environment': 'http://environment.independent.co.uk/index.jsp?service=rss',
	'      Climate Change': 'http://environment.independent.co.uk/climate_change/index.jsp?service=rss',
#	'      Lifestyle': 'http://environment.independent.co.uk/lifestyle/index.jsp?service=rss',	# BUSTED (404)
#	'      Wildlife': 'http://environment.independent.co.uk/wildlife/index.jsp?service=rss',	# BUSTED (404)
	'    Sport': 'http://sport.independent.co.uk/index.jsp?service=rss',
	'      Cricket': 'http://sport.independent.co.uk/cricket/index.jsp?service=rss',
	'      Football': 'http://sport.independent.co.uk/football/index.jsp?service=rss',
	'        Premiership': 'http://sport.independent.co.uk/football/premiership/index.jsp?service=rss',
	'        News': 'http://sport.independent.co.uk/football/news/index.jsp?service=rss',
	'        Comment': 'http://sport.independent.co.uk/football/comment/index.jsp?service=rss',
	'        European': 'http://sport.independent.co.uk/football/european/index.jsp?service=rss',
	'        Internationals': 'http://sport.independent.co.uk/football/internationals/index.jsp?service=rss',
	'        Coca Cola': 'http://sport.independent.co.uk/football/coca_cola/index.jsp?service=rss',
	'        Scotland': 'http://sport.independent.co.uk/football/scotland/index.jsp?service=rss',
	'      General': 'http://sport.independent.co.uk/general/index.jsp?service=rss',
#	'      Golf': 'http://sport.independent.co.uk/golf/index.jsp?service=rss',			# BUSTED (404)
	'      Motor Racing': 'http://sport.independent.co.uk/motor_racing/index.jsp?service=rss',
	'      Rugby League': 'http://sport.independent.co.uk/rugby_league/index.jsp?service=rss',
	'      Rugby Union': 'http://sport.independent.co.uk/rugby_union/index.jsp?service=rss',
	'      Tennis': 'http://sport.independent.co.uk/tennis/index.jsp?service=rss',
#	'      Olympics': 'http://sport.independent.co.uk/olympics/index.jsp?service=rss',	# BUSTED (404)
	'    Comment': 'http://comment.independent.co.uk/index.jsp?service=rss',
	'      Leading Articles': 'http://comment.independent.co.uk/leading_articles/index.jsp?service=rss',
	'      Letters': 'http://comment.independent.co.uk/letters/index.jsp?service=rss',
	'      Commentators': 'http://comment.independent.co.uk/commentators/index.jsp?service=rss',

	# Individual columnist feeds are all busted (404)...
	# but they are aggregated in other feeds so not a problem.

#	'      Columnists A-L': 'http://comment.independent.co.uk/columnists_a_l/index.jsp?service=rss',
#	'        Yasmin Alibhai-Brown': 'http://comment.independent.co.uk/columnists_a_l/yasmin_alibhai_brown/index.jsp?service=rss',
#	'        Bruce Anderson': 'http://comment.independent.co.uk/columnists_a_l/bruce_anderson/index.jsp?service=rss',
#	'        Joan Bakewell': 'http://comment.independent.co.uk/columnists_a_l/joan_bakewell/index.jsp?service=rss',
#	'        Terence Blacker': 'http://comment.independent.co.uk/columnists_a_l/terence_blacker/index.jsp?service=rss',
#	'        Simon Carr': 'http://comment.independent.co.uk/columnists_a_l/simon_carr/index.jsp?service=rss',
#	'        Mary Dejevsky': 'http://comment.independent.co.uk/columnists_a_l/mary_dejevsky/index.jsp?service=rss',
#	'        Tracey Emin': 'http://comment.independent.co.uk/columnists_a_l/tracey_emin/index.jsp?service=rss',
#	'        Helen Fielding': 'http://comment.independent.co.uk/columnists_a_l/helen_fielding/index.jsp?service=rss',
#	'        Andrew Grice': 'http://comment.independent.co.uk/columnists_a_l/andrew_grice/index.jsp?service=rss',
#	'        Adrian Hamilton': 'http://comment.independent.co.uk/columnists_a_l/adrian_hamilton/index.jsp?service=rss',
#	'        Johann Hari': 'http://comment.independent.co.uk/columnists_a_l/johann_hari/index.jsp?service=rss',
#	'        Philip Hensher': 'http://comment.independent.co.uk/columnists_a_l/philip_hensher/index.jsp?service=rss',
#	'        Howard Jacobson': 'http://comment.independent.co.uk/columnists_a_l/howard_jacobson/index.jsp?service=rss',
#	'        Alex James': 'http://comment.independent.co.uk/columnists_a_l/alex_james/index.jsp?service=rss',
#	'        Dom Joly': 'http://comment.independent.co.uk/columnists_a_l/dom_joly/index.jsp?service=rss',
#	'        Miles Kington': 'http://comment.independent.co.uk/columnists_a_l/miles_kington/index.jsp?service=rss',
#	'        Dominic Lawson': 'http://comment.independent.co.uk/columnists_a_l/dominic_lawson/index.jsp?service=rss',
#	'        David Lister': 'http://comment.independent.co.uk/columnists_a_l/david_lister/index.jsp?service=rss',
#	'      Columnists M-Z': 'http://comment.independent.co.uk/columnists_m_z/index.jsp?service=rss',
#	'        Donald Macintyre': 'http://comment.independent.co.uk/columnists_m_z/donald_macintyre/index.jsp?service=rss',
#	'        Hamish McRae': 'http://comment.independent.co.uk/columnists_m_z/hamish_mcrae/index.jsp?service=rss',
#	'        Matthew Norman': 'http://comment.independent.co.uk/columnists_m_z/matthew_norman/index.jsp?service=rss',
#	'        Deborah Orr': 'http://comment.independent.co.uk/columnists_m_z/deborah_orr/index.jsp?service=rss',
#	'        Christina Patterson': 'http://comment.independent.co.uk/columnists_m_z/christina_patterson/index.jsp?service=rss',
#	'        Rowan Pelling': 'http://comment.independent.co.uk/columnists_m_z/rowan_pelling/index.jsp?service=rss',
#	'        John Rentoul': 'http://comment.independent.co.uk/columnists_m_z/john_rentoul/index.jsp?service=rss',
#	'        Steve Richards': 'http://comment.independent.co.uk/columnists_m_z/steve_richards/index.jsp?service=rss',
#	'        Deborah Ross': 'http://comment.independent.co.uk/columnists_m_z/deborah_ross/index.jsp?service=rss',
#	'        Will Self': 'http://comment.independent.co.uk/columnists_m_z/will_self/index.jsp?service=rss',
#	'        Joan Smith': 'http://comment.independent.co.uk/columnists_m_z/joan_smith/index.jsp?service=rss',
#	'        Mark Steel': 'http://comment.independent.co.uk/columnists_m_z/mark_steel/index.jsp?service=rss',
#	'        Janet Street-Porter': 'http://comment.independent.co.uk/columnists_m_z/janet_street_porter/index.jsp?service=rss',
#	'        Thomas Sutcliffe': 'http://comment.independent.co.uk/columnists_m_z/thomas_sutcliffe/index.jsp?service=rss',
#	'        Brian Viner': 'http://comment.independent.co.uk/columnists_m_z/brian_viner/index.jsp?service=rss',
#	'        John Walsh': 'http://comment.independent.co.uk/columnists_m_z/john_walsh/index.jsp?service=rss',
#	'        Alan Watkins': 'http://comment.independent.co.uk/columnists_m_z/alan_watkins/index.jsp?service=rss',
#	'        Andreas Whittam Smith': 'http://comment.independent.co.uk/columnists_m_z/andreas_whittam_smith/index.jsp?service=rss',

	# this one isn't an rss feed! It' just goes to the edutcation section
#	'    Education': 'http://education.independent.co.uk/index.jsp?service=rss',

	# this one does general news rather than education news	
#	'      News': 'http://education.independent.co.uk/news/index.jsp?service=rss',

	# these are all busted (404):
#	'      Clearing': 'http://education.independent.co.uk/clearing/index.jsp?service=rss',
#	'      Higher': 'http://education.independent.co.uk/higher/index.jsp?service=rss',
#	'        A-Z Unis & Colleges ': 'http://education.independent.co.uk/higher/az_uni_colleges/index.jsp?service=rss',
#	'        A-Z Degrees': 'http://education.independent.co.uk/higher/az_degrees/index.jsp?service=rss',
#	'        Advice': 'http://education.independent.co.uk/higher/advice/index.jsp?service=rss',
#	'        Overseas Students': 'http://education.independent.co.uk/higher/overseas_students/index.jsp?service=rss',
#	'      Careers Advice': 'http://education.independent.co.uk/careers_advice/index.jsp?service=rss',
#	'        A-Z Careers': 'http://education.independent.co.uk/careers_advice/az_careers/index.jsp?service=rss',
#	'        Aerospace': 'http://education.independent.co.uk/careers_advice/aerospace/index.jsp?service=rss',
#	'        Engineering': 'http://education.independent.co.uk/careers_advice/engineering/index.jsp?service=rss',
#	'        Featured Institutions': 'http://education.independent.co.uk/careers_advice/featured_institutions/index.jsp?service=rss',
#	'      Gap Year': 'http://education.independent.co.uk/gap_year/index.jsp?service=rss',
#	'        Suppliers': 'http://education.independent.co.uk/gap_year/suppliers/index.jsp?service=rss',
#	'      Graduate Options': 'http://education.independent.co.uk/graduate_options/index.jsp?service=rss',
#	'        Business Schools': 'http://education.independent.co.uk/graduate_options/business_schools/index.jsp?service=rss',
#	'        MBAs Guide': 'http://education.independent.co.uk/graduate_options/mbas_guide/index.jsp?service=rss',
#	'      Further': 'http://education.independent.co.uk/further/index.jsp?service=rss',
#	'      Schools': 'http://education.independent.co.uk/schools/index.jsp?service=rss',
#	'        A-Z A-levels': 'http://education.independent.co.uk/schools/az-alevels/index.jsp?service=rss',
#	'      Magazines': 'http://education.independent.co.uk/magazines/index.jsp?service=rss',

	'    Money': 'http://money.independent.co.uk/index.jsp?service=rss',
	'      Property': 'http://money.independent.co.uk/property/index.jsp?service=rss',
	'        Mortgages': 'http://money.independent.co.uk/property/mortgages/index.jsp?service=rss',
	'        Homes': 'http://money.independent.co.uk/property/homes/index.jsp?service=rss',
#	'        Finder': 'http://money.independent.co.uk/property/finder/index.jsp?service=rss',	# BUSTED (404)
	'      Personal Finance': 'http://money.independent.co.uk/personal_finance/index.jsp?service=rss',
		# irrelevant? empty at time of writing anyway...
#	'        Financial Directory': 'http://money.independent.co.uk/personal_finance/financial_directory/index.jsp?service=rss',
	'        Invest & Save': 'http://money.independent.co.uk/personal_finance/invest_save/index.jsp?service=rss',
	'        Loans & Credit': 'http://money.independent.co.uk/personal_finance/loans_credit/index.jsp?service=rss',
	'        Pensions': 'http://money.independent.co.uk/personal_finance/pensions/index.jsp?service=rss',
	'        Insurance': 'http://money.independent.co.uk/personal_finance/insurance/index.jsp?service=rss',
	'        Tax': 'http://money.independent.co.uk/personal_finance/tax/index.jsp?service=rss',
	'    Travel': 'http://travel.independent.co.uk/index.jsp?service=rss',
	'      News & Advice': 'http://travel.independent.co.uk/news_and_advice/index.jsp?service=rss',
	'      Biztravel': 'http://travel.independent.co.uk/biztravel/index.jsp?service=rss',
	'      Skiing': 'http://travel.independent.co.uk/skiing/index.jsp?service=rss',
	'      Asia': 'http://travel.independent.co.uk/asia/index.jsp?service=rss',
	'      Africa': 'http://travel.independent.co.uk/africa/index.jsp?service=rss',
	'      Americas': 'http://travel.independent.co.uk/americas/index.jsp?service=rss',
	'      Australasia & Pacific': 'http://travel.independent.co.uk/ausandpacific/index.jsp?service=rss',
	'      Europe': 'http://travel.independent.co.uk/europe/index.jsp?service=rss',
	'      Middle East': 'http://travel.independent.co.uk/middle_east/index.jsp?service=rss',
	'      UK': 'http://travel.independent.co.uk/uk/index.jsp?service=rss',
	'    Arts': 'http://arts.independent.co.uk/index.jsp?service=rss',
	'      Books': 'http://arts.independent.co.uk/books/index.jsp?service=rss',
	'        News': 'http://arts.independent.co.uk/books/news/index.jsp?service=rss',
	'        Reviews': 'http://arts.independent.co.uk/books/reviews/index.jsp?service=rss',
	'        Features': 'http://arts.independent.co.uk/books/features/index.jsp?service=rss',
	'      Film': 'http://arts.independent.co.uk/film/index.jsp?service=rss',
	'        News': 'http://arts.independent.co.uk/film/news/index.jsp?service=rss',
	'        Reviews': 'http://arts.independent.co.uk/film/reviews/index.jsp?service=rss',
	'        Features': 'http://arts.independent.co.uk/film/features/index.jsp?service=rss',
	'      Music': 'http://arts.independent.co.uk/music/index.jsp?service=rss',
	'        News': 'http://arts.independent.co.uk/music/news/index.jsp?service=rss',
	'        Reviews': 'http://arts.independent.co.uk/music/reviews/index.jsp?service=rss',
	'        Features': 'http://arts.independent.co.uk/music/features/index.jsp?service=rss',
	'      Theatre': 'http://arts.independent.co.uk/theatre/index.jsp?service=rss',
	'        News': 'http://arts.independent.co.uk/theatre/news/index.jsp?service=rss',
	'        Reviews': 'http://arts.independent.co.uk/theatre/reviews/index.jsp?service=rss',
	'        Features': 'http://arts.independent.co.uk/theatre/features/index.jsp?service=rss',
	'    Living': 'http://www.independent.co.uk/living/index.jsp?service=rss',
			# these three are busted (404)
#	'      Dating': 'http://www.independent.co.uk/living/dating/index.jsp?service=rss',
#	'      Gaming': 'http://www.independent.co.uk/living/gaming/index.jsp?service=rss',
#	'      Offers': 'http://www.independent.co.uk/living/offers/index.jsp?service=rss',
	'      Food & Drink': 'http://www.independent.co.uk/living/food_and_drink/index.jsp?service=rss',
	'        News': 'http://www.independent.co.uk/living/food_and_drink/news/index.jsp?service=rss',
	'        Reviews': 'http://www.independent.co.uk/living/food_and_drink/reviews/index.jsp?service=rss',
	'        Features': 'http://www.independent.co.uk/living/food_and_drink/features/index.jsp?service=rss',
	'        Recipes': 'http://www.independent.co.uk/living/food_and_drink/recipes/index.jsp?service=rss',
	'      Motoring': 'http://www.independent.co.uk/living/motoring/index.jsp?service=rss',
	'        Features': 'http://www.independent.co.uk/living/motoring/features/index.jsp?service=rss',
	'        Road Tests': 'http://www.independent.co.uk/living/motoring/road_tests/index.jsp?service=rss',
	'        Comment': 'http://www.independent.co.uk/living/motoring/comment/index.jsp?service=rss',
#	'        Used Cars': 'http://www.independent.co.uk/living/motoring/used_cars/index.jsp?service=rss',	# BUSTED (404)

	# not sure about classified... should we deal with these?
#	'    Classified': 'http://classified.independent.co.uk/index.jsp?service=rss',
#	'      Property': 'http://classified.independent.co.uk/property/index.jsp?service=rss',
#	'      Travel': 'http://classified.independent.co.uk/travel/index.jsp?service=rss',
#	'      Cars': 'http://classified.independent.co.uk/cars/index.jsp?service=rss',
#	'      Entertainment': 'http://classified.independent.co.uk/entertainment/index.jsp?service=rss',
#	'      Lifestyle': 'http://classified.independent.co.uk/lifestyle/index.jsp?service=rss',
#	'      Jobs': 'http://classified.independent.co.uk/jobs/index.jsp?service=rss',
	}



def Extract( html, context ):
	"""Parse the html of a single article

	html -- the article html
	context -- any extra info we have about the article (from the rss feed)
	"""

	art = context

	soup = BeautifulSoup( html )

	# if we don't have a description, try the deckheader meta tag...
	# <meta name="icx_deckheader" content="Stars of reality TV &ndash; and now the culprits blamed for spreading disease" />
	if not 'description' in art:
		art['description'] = u''
	if not art['description'].strip():
		deckheader = soup.find( 'meta', {'name':'icx_deckheader'} )
		if deckheader:
			art['description'] = ukmedia.FromHTML( deckheader['content'] )
			#print "DECKHEADER: '%s'" % (art['description'])

	articlediv = soup.find( 'div', { 'class':'article' } )

	headline = articlediv.find( 'h1' )
	for cruft in headline.findAll( 'span' ):
		cruft.extract()
	art[ 'title' ] = headline.renderContents(None).strip()
	art[ 'title' ] = ukmedia.FromHTML( art['title'] )

	bylinepart = articlediv.find( 'h3' )
	if bylinepart:
		byline = bylinepart.renderContents(None).strip()
	else:
		byline = u''

	# for comment pages - if byline is empty, try and get it from title
	author_maybe_in_headline = 0
	comment_section_prefixes = [
		'http://comment.independent.co.uk', 
		'http://news.independent.co.uk/fisk',	# special case for Robert Fisk
		'http://sport.independent.co.uk/football/comment',
		'http://www.independent.co.uk/living/motoring/comment',
		]

	for prefix in comment_section_prefixes:
		if art['srcurl'].startswith( prefix ):
			author_maybe_in_headline = 1

	if byline == u'' and author_maybe_in_headline:
		# eg "Janet Street-Porter: Our politicians know nothing of real life"
		m = re.match( "([\\w\\-']+\\s+[\\w\\-']+(\\s+[\\w\\-']+)?\\s*):", art['title'], re.UNICODE )
		if m:
			byline = m.group(1)
			# cull out duds
			if byline.lower() in ( u'leading article', u'the third leader' ):
				byline = u''


	art[ 'byline' ] = ukmedia.FromHTML( byline )

	pubdate = articlediv.find( 'h4' )
	art[ 'pubdate' ] = CrackDate( pubdate.renderContents() )

	body = articlediv.find( 'div', id='bodyCopyContent' )

	# remove the "Interesting? Click here to explore further" link
	cruft = body.find( 'a', id=re.compile("^proximic_proxit") )
	if cruft:
		cruft.extract()

	art['content'] = body.renderContents( None )
	art['content'] = ukmedia.SanitiseHTML( art['content'] )

	# if we still don't have any description, use first para
	if art['description'] == u'':
		art['description'] = ukmedia.FromHTML( body.p.renderContents(None) )
		#print "FIRSTPARA: '%s'" %(art['description'])

	return art



# TODO: replace with ukmedia generic dateparser
def CrackDate( raw ):
	""" return datetime, or None if matching fails
	
	example date string: 'Published:&nbsp;01 September 2006'
	"""

	datepat = re.compile( '([0-9]{2})\s+(\w+)\s+([0-9]{4})' )
	m = datepat.search( raw )
	if not m:
		return None
	day = int( m.group(1) )
	month = ukmedia.MonthNumber( m.group(2) )
	year = int( m.group(3) )

	return datetime( year,month,day )





def ScrubFunc( context, entry ):
	""" description contains html entities and tags...  scrub it! """
	context[ 'description' ] = ukmedia.FromHTML( context['description'] )
	return context



def ContextFromURL( url ):
	"""Build up an article scrape context from a bare url."""
	context = {}
	context['srcurl'] = url
	context['permalink'] = url
	context[ 'srcid' ] = url
	context['srcorgname'] = u'independent'
	context['lastseen'] = datetime.now()
	return context


def main():
	parser = OptionParser()
	parser.add_option( "-u", "--url", dest="url", help="scrape a single article from URL", metavar="URL" )
	parser.add_option("-d", "--dryrun", action="store_true", dest="dryrun", help="don't touch the database")

	(options, args) = parser.parse_args()

	found = []
	if options.url:
		context = ContextFromURL( options.url )
		found.append( context )
	else:
		found = found + ukmedia.FindArticlesFromRSS( rssfeeds, u'independent', ScrubFunc )

	if options.dryrun:
		store = ArticleDB.DummyArticleDB()	# testing
	else:
		store = ArticleDB.ArticleDB()

	ukmedia.ProcessArticles( found, store, Extract )

	return 0

if __name__ == "__main__":
    sys.exit(main())

