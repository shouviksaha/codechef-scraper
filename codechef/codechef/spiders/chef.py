from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from codechef.items import Problem,Solution
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import HTMLParser
import os

class CodechefSpider(CrawlSpider):
	name = "codechef_crawler"
	allowed_domains = ["codechef.com"]
	start_urls = ["http://www.codechef.com/problems/easy/","http://www.codechef.com/problems/medium/","http://www.codechef.com/problems/hard/","http://www.codechef.com/problems/challenege/"]
	
	rules = (Rule(SgmlLinkExtractor(allow=('/problems/[A-Z,0-9,-]+')), callback='parse_item'),)

	def parse_ptsol(self,response):
		item = Solution()
		hxs = HtmlXPathSelector(response)
		code = hxs.select("//pre/text()").extract()
		item['code']= code[0]
		f = open('problems/'+response.meta['name']+'/'+response.meta['count']+'.txt','wb')
		h = HTMLParser.HTMLParser()
		f.write((h.unescape(code[0])).encode("utf-8"))
		f.close()
		return item
	
	def parse_solutions(self,response):
		hxs = HtmlXPathSelector(response)
		x = hxs.select("//tr[@class='kol']//td[8]/ul/li/a/@href").extract()
		filename = response.meta['name']
		for i in range(10):
			request = Request('http://www.codechef.com/viewplaintext/'+x[i].split('/')[-1], callback=self.parse_ptsol)
			request.meta['name'] = filename
			request.meta['count'] = str(i)
			yield request
		
	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = Problem()
		item['title'] = hxs.select("//table[@class='pagetitle-prob']/tr/td/h1/text()").extract()
		item['content'] = hxs.select("//div[@class='node clear-block']//div[@class='content']").extract()
		filename = str(item['title'][0])
		solutions_url = 'http://www.codechef.com/status/' + response.url.split('/')[-1] + '?language=All&status=15&handle=&sort_by=Time&sorting_order=asc'
		request = Request(solutions_url,  callback=self.parse_solutions)
		request.meta['name'] = filename
		yield request
		if not os.path.exists('problems'): os.makedirs('problems')
		if not os.path.exists('problems/'+filename): os.makedirs('problems/'+filename)
		f = open('problems/' + filename+'/question.html','wb')
		f.write('<head>')
		f.write('<meta charset="UTF-8">')
		f.write('</head>')
		f.write("<div style='width:800px;margin:50px'>")
		for i in item['content']:
			f.write(i.encode("utf-8"))
		f.write("</div>")
		f.close()





