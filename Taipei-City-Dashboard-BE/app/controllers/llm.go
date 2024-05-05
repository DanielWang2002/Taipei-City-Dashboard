package controllers

import (
    "net/http"
	"github.com/gin-gonic/gin"
    "bytes"
    "io/ioutil"
    "log"
)

func HandleLLMRequest(c *gin.Context) {
    w := c.Writer
    r := c.Request
    jsonRPCServerURL := "http://json_rpc_server:5555"
    // 假設你從前端收到的數據是以 JSON 格式在請求體中
    requestBody, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading request body", http.StatusInternalServerError)
        return
    }

    resp, err := http.Post(jsonRPCServerURL, "application/json", bytes.NewBuffer(requestBody))
    if err != nil {
        log.Fatalf("Error contacting JSON RPC server: %v", err)
        http.Error(w, "Error contacting JSON RPC server", http.StatusInternalServerError)
        return
    }
    defer resp.Body.Close()
    responseBody, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        http.Error(w, "Error reading response body", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.Write(responseBody)
}
