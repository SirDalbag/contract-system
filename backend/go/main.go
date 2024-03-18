// https://github.com/bogdandrienko/awesome-golang/tree/main/1_base

package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

type Answer struct {
	Ip   string `json:"ip"`
	Date int    `json:"date"`
}

func formattedDate(str_format string, _datetime int64) (string, error) {
	t := time.Unix(_datetime, 0)
	switch str_format {
	case "%04d_%02d_%02d_%02d":
		return fmt.Sprintf(str_format, t.Year(), t.Month(), t.Day(), t.Hour()), nil
	case "%04d_%02d_%02d":
		return fmt.Sprintf(str_format, t.Year(), t.Month(), t.Day()), nil
	default:
		return "", nil
	}
}

func writeTxtComplex(ip string, date int) error {
	formatted_str, err := formattedDate("%04d_%02d_%02d_%02d", 1710773281)
	if err != nil {
		return err
	}
	filename := fmt.Sprintf("%s.txt", formatted_str)
	file, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE, 0644)
	if err != nil {
		return err
	}
	defer func(file *os.File) {
		err := file.Close()
		if err != nil {

			return
		}
	}(file)
	_, err = file.WriteString(fmt.Sprintf("%s %d\n", ip, date))
	if err != nil {
		return err
	}
	return nil
}

func main() {
	// var ip string = "192.168.0.1"
	// var date int     = 1710773281
	router := gin.Default()
	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "OK"})
	})
	router.POST("/api/log", func(c *gin.Context) {
		var answer Answer
		raw, err := c.GetRawData()
		if err != nil {
			fmt.Println(err)
			return
		}
		raw_str := string(raw)
		raw_list := strings.Split(raw_str, "&")
		// ip=127.0.0.1&date=1710779172
		for _, raw_item := range raw_list {
			raw_item_list := strings.Split(raw_item, "=")
			if len(raw_item_list) != 2 {
				continue
			}
			if raw_item_list[0] == "ip" {
				answer.Ip = raw_item_list[1]
			} else if raw_item_list[0] == "date" {
				date, err := strconv.Atoi(raw_item_list[1])
				if err != nil {
					fmt.Println(err)
					return
				}
				answer.Date = date
			}
		}
		if answer.Ip == "" || answer.Date == 0 {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Bad request"})
			return
		}
		// if err := c.BindJSON(&answer); err != nil {
		// 	fmt.Println(err)
		// 	c.JSON(http.StatusBadRequest, gin.H{"error": "Ошибка 1"})
		// 	return
		// }
		err = writeTxtComplex(answer.Ip, answer.Date)
		if err != nil {
			fmt.Println(err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Ошибка 2"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": "OK"})
	})

	router.Run(":8001")
}
