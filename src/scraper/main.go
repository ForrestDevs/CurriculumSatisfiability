package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"github.com/gocolly/colly"
)

func main() {
	c := colly.NewCollector(colly.AllowedDomains("www.cs.queensu.ca", "cs.queensu.ca"))

	c.OnRequest(func(r *colly.Request) {
		r.Headers.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
		fmt.Println("Visiting", r.URL.String())
	})

	c.OnResponse(func(r *colly.Response) {
		if r.StatusCode == 404 {
			fmt.Println("404")
		} else {
			fmt.Println("Visited", r.Request.URL)
		}
	})

	c.OnHTML("h1", func(e *colly.HTMLElement) {
		if strings.Contains(e.Text, "404") {
			return
		}

		// Open file in append mode.
		f, err := os.OpenFile("scraper/output.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer f.Close()

		// Write first 8 characters of e.Text to the file.
		if _, err := f.WriteString(e.Text[:8] + "\n"); err != nil {
			fmt.Println(err)
		}
	})

	baseURL := "https://www.cs.queensu.ca/undergraduate/courses/CISC-"
	for i := 100; i <= 499; i++ {
		c.Visit(baseURL + strconv.Itoa(i))
	}

	c.Visit("https://www.cs.queensu.ca/undergraduate/courses/COCA-201")
	c.Visit("https://www.cs.queensu.ca/undergraduate/courses/COGS-100")
	c.Visit("https://www.cs.queensu.ca/undergraduate/courses/COGS-201")
	c.Visit("https://www.cs.queensu.ca/undergraduate/courses/COGS-300")
	c.Visit("https://www.cs.queensu.ca/undergraduate/courses/COGS-400")
	c.Visit("https://www.cs.queensu.ca/undergraduate/courses/COGS-499")
}