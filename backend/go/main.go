package main

import (
	"database/sql"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

type Task struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Status string `json:"status"`
}

var db *sql.DB

func main() {
	var err error
	db, err = sql.Open("postgres", "user=postgres dbname=storage password=admin sslmode=disable")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	router := gin.Default()

	router.POST("/task", createTask)
	router.GET("/tasks", getTasks)
	router.GET("/tasks/:id", getTask)
	router.PUT("/tasks/:id", updateTask)
	router.DELETE("/tasks/:id", deleteTask)

	router.Run(":8080")
}

func createTask(c *gin.Context) {
	var task Task
	if err := c.BindJSON(&task); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err := db.QueryRow("INSERT INTO go_task (title, status) VALUES($1, $2) RETURNING id", task.Title, task.Status).Scan(&task.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error creating task"})
		return
	}

	c.JSON(http.StatusCreated, task)
}

func getTasks(c *gin.Context) {
	rows, err := db.Query("SELECT id, title, status FROM go_task")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error fetching tasks"})
		return
	}
	defer rows.Close()

	tasks := []Task{}
	for rows.Next() {
		var task Task
		if err := rows.Scan(&task.ID, &task.Title, &task.Status); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error scanning tasks"})
			return
		}
		tasks = append(tasks, task)
	}

	c.JSON(http.StatusOK, tasks)
}

func getTask(c *gin.Context) {
	id := c.Param("id")
	var task Task
	err := db.QueryRow("SELECT id, title, status FROM go_task WHERE id = $1", id).Scan(&task.ID, &task.Title, &task.Status)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error fetching task"})
		return
	}

	c.JSON(http.StatusOK, task)
}

func updateTask(c *gin.Context) {
	id := c.Param("id")
	var task Task
	if err := c.BindJSON(&task); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err := db.Exec("UPDATE go_task SET title=$1, status=$2 WHERE id=$3", task.Title, task.Status, id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error updating task"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Task updated successfully"})
}

func deleteTask(c *gin.Context) {
	id := c.Param("id")

	_, err := db.Exec("DELETE FROM go_task WHERE id=$1", id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error deleting task"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Task deleted successfully"})
}
