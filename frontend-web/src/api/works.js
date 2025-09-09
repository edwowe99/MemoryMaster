import axiosInstance from "../contexts/axiosInstance";

export async function fetchWorks() {
    try {
        const response = await axiosInstance.get("/works/");
        return response.data;
    } catch (error) {
        console.error("Error fetching works:", error);
        throw error;
    }
}

export async function fetchWorkBySlug(slug) {
    const response = await axiosInstance.get(`/works/${slug}/`);
    return response.data;
}

export async function postPracticeResults(workId, units) {
  const res = await axiosInstance.post("/practice-result/", {
    work_id: workId,
    mode: "practice", // or "test"/"repetition"
    units: units,
  });
  return res.data; // axios automatically parses JSON
}