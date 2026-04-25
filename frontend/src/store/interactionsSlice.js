import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { apiClient } from "../api/client";

export const fetchInteractions = createAsyncThunk("interactions/fetchAll", async () => {
  const res = await apiClient.get("/api/interactions");
  return res.data;
});

export const createInteraction = createAsyncThunk("interactions/create", async (payload) => {
  const res = await apiClient.post("/api/interactions", payload);
  return res.data;
});

export const updateInteraction = createAsyncThunk(
  "interactions/update",
  async ({ id, payload }) => {
    const res = await apiClient.put(`/api/interactions/${id}`, payload);
    return res.data;
  }
);

const interactionsSlice = createSlice({
  name: "interactions",
  initialState: {
    items: [],
    status: "idle",
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.items.unshift(action.payload);
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        state.items = state.items.map((item) =>
          item.id === action.payload.id ? action.payload : item
        );
      });
  }
});

export default interactionsSlice.reducer;

