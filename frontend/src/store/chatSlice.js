import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { apiClient } from "../api/client";

export const sendChatMessage = createAsyncThunk("chat/send", async (payload) => {
  const res = await apiClient.post("/api/agent/chat", payload);
  return res.data;
});

const chatSlice = createSlice({
  name: "chat",
  initialState: {
    messages: [
      {
        id: "welcome",
        role: "assistant",
        content:
          "I can log interactions, edit records, suggest next-best actions, and draft follow-ups."
      }
    ],
    status: "idle",
    error: null
  },
  reducers: {
    pushUserMessage(state, action) {
      state.messages.push(action.payload);
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.status = "loading";
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.messages.push({
          id: crypto.randomUUID(),
          role: "assistant",
          content: action.payload.response,
          trace: action.payload.trace
        });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
        state.messages.push({
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Copilot request failed. Please make sure backend is running on http://localhost:8000."
        });
      });
  }
});

export const { pushUserMessage } = chatSlice.actions;
export default chatSlice.reducer;
