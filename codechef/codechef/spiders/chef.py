from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from codechef.items import Problem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class CodechefSpider(CrawlSpider):
	name = "codechef_crawler"
	allowed_domains = ["codechef.com"]
	start_urls = ["http://www.codechef.com/problems/easy/","http://www.codechef.com/problems/medium/","http://www.codechef.com/problems/hard/","http://www.codechef.com/problems/challenege/"]
	
	rules = (Rule(SgmlLinkExtractor(allow=('/problems/[A-Z]+')), callback='parse_item'),)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = Problem()
		item['title'] = hxs.select("//table[@class='pagetitle-prob']/tr/td/h1/text()").extract()
		item['content'] = hxs.select("//div[@class='node clear-block']//div[@class='content']").extract()
		filename = str(item['title'][0])
		f = open('problems/'+filename+'.html','wb')
		f.write("<div style='width:800px;margin:50px'>")
		for i in item['content']:
			f.write(i.encode("utf-8"))
		f.write("</div>")
		f.close()





