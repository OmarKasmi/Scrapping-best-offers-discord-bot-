import bs4
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent 
from discord.ext import commands
import requests
user = UserAgent()
options = Options()
options.add_argument("user-agent="+user.random)
driver = webdriver.Chrome(options=options)
driver.get("https://www.ordinateur-occasion.com/100-promo-ordinateur-portable?order=product.price.asc")

html = driver.page_source
soup = bs4.BeautifulSoup(html,"html.parser")
 
items = soup.select('article > div > div > a')

saved_images = []
title = []
price = []
for item in soup.select('.product-desc-wrap > .product-description > h3 > a'):
    	title.append(item.text)




for item in soup.select('.price'):
    	price.append(item.text)




bot = commands.Bot(command_prefix = "!")
@bot.command()
async def all_product(ctx):
	our_images_list=[]
	image = soup.select('article > div > div > a > img')
	for i in image:
		images = image.index(i)
		image_info = image[images]
		get_image = requests.get(image_info['data-full-size-image-url']).content
		saved_images.append(get_image)
		f = open('image '+ str(image.index(i))+'.jpg','wb')
		f = f.write(get_image)
		our_images_list.append(f)
		with open('image '+ str(image.index(i))+'.jpg','rb') as fh:
			f= discord.File(fh, filename ='image '+ str(image.index(i))+'.jpg')
		await ctx.send(file=f)
		await ctx.send(title[images])
		await ctx.send(price[images][0:5] + "€")
	await ctx.message.delete()

@bot.command()
async def BestOffer(ctx):
	our_images_list=[]
	image = soup.select('article > div > div > a > img')
	image_info = image[0]
	get_image = requests.get(image_info['data-full-size-image-url']).content
	saved_images.append(get_image)
	f = open('image 0.jpg','wb')
	f = f.write(get_image)
	our_images_list.append(f)
	with open('image 0.jpg','rb') as fh:
		best_offer_image = discord.File(fh, filename ='image 0.jpg')
	await ctx.send(file= best_offer_image)
	await ctx.send(title[0])
	await ctx.send(price[0][0:5] + "€")
	await ctx.message.delete()



bot.run("")
