// github.com/bogdandrienko/awesome-golang/

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

func formattedDate(str_format string, _datetime int) (string, error) {
	t := time.Unix(int64(_datetime), 0)
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
	formatted_str, err := formattedDate("%04d_%02d_%02d_%02d", date)
	if err != nil {
		return err
	}
	_, err = os.Stat("logs")
	if os.IsNotExist(err) {
		err := os.Mkdir("logs", os.ModePerm)
		if err != nil {
			return err
		}
	}
	filename := fmt.Sprintf("logs/%s.txt", formatted_str)
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
	router := gin.Default()
	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "OK"})
	})
	router.POST("/api/log", func(c *gin.Context) {
		var answer Answer
		raw, err := c.GetRawData()
		if err != nil {
			return
		}
		_raw := strings.Split(string(raw), "&")
		for _, item := range _raw {
			item_list := strings.Split(item, "=")
			if len(item_list) != 2 {
				continue
			}
			if item_list[0] == "ip" {
				answer.Ip = item_list[1]
			} else if item_list[0] == "date" {
				date, err := strconv.Atoi(item_list[1])
				if err != nil {
					return
				}
				answer.Date = date
			}
		}
		if answer.Ip == "" || answer.Date == 0 {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Bad request"})
			return
		}
		err = writeTxtComplex(answer.Ip, answer.Date)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Error"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"data": "OK"})
	})

	router.Run(":8001")
}
