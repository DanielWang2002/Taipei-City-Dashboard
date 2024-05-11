package controllers

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

type JSONRPCResponse struct {
	ID      int    `json:"id"`
	JSONRPC string `json:"jsonrpc"`
	Result  string `json:"result"`
}

type Response struct {
	Role   string `json:"role"`
	Result string `json:"result"`
}

func HandleLLMRequest(c *gin.Context) {
	w := c.Writer
	r := c.Request
	jsonRPCServerURL := "http://json_rpc_server:5555"

	requestBody, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}

	resp, err := http.Post(jsonRPCServerURL, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		log.Printf("Error contacting JSON RPC server: %v", err)
		http.Error(w, "Error contacting JSON RPC server", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "Error reading response body", http.StatusInternalServerError)
		return
	}

	var rpcResp JSONRPCResponse
	if err := json.Unmarshal(responseBody, &rpcResp); err != nil {
		http.Error(w, "Error parsing JSON response", http.StatusInternalServerError)
		return
	}

	responseStruct := Response{
		Role:   "tpe",
		Result: rpcResp.Result,
	}

	jsonResponse, err := json.Marshal(responseStruct)
	if err != nil {
		http.Error(w, "Error marshalling JSON", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonResponse)
}
