import streamlit as st

# Initialize the counter for merge sort in session state
if "merge_count" not in st.session_state:
    st.session_state.merge_count = 0

def mergeSort(numberArray):
    st.session_state.merge_count += 1
    st.markdown(f"**Iteration {st.session_state.merge_count}**")
    if(len(numberArray) > 1):

        #split the array into left and right arrays
        leftArray = numberArray[ : len(numberArray) // 2]
        rightArray = numberArray[len(numberArray) // 2 :]

        st.text(f"Left Subarray: {leftArray}")
        st.text(f"Right Subarray: {rightArray}")

        #Pass the subarrays to the recursive call to further split the array
        mergeSort(leftArray)
        mergeSort(rightArray)

        #Merge the subarrays
        arrayIndex = leftArrayIndex = rightArrayIndex = 0
        while leftArrayIndex < len(leftArray) and rightArrayIndex < len(rightArray):
            if(leftArray[leftArrayIndex] < rightArray[rightArrayIndex]):
                numberArray[arrayIndex] = leftArray[leftArrayIndex]
                leftArrayIndex += 1
            else:
                numberArray[arrayIndex] = rightArray[rightArrayIndex]
                rightArrayIndex += 1
            arrayIndex += 1

        #Copy leftover elements from left subarray to the array
        while leftArrayIndex < len(leftArray):
            numberArray[arrayIndex] = leftArray[leftArrayIndex]
            leftArrayIndex += 1
            arrayIndex += 1
        
        #Copy leftover elements from the right subarray to the array
        while rightArrayIndex < len(rightArray):
            numberArray[arrayIndex] = rightArray[rightArrayIndex]
            rightArrayIndex += 1
            arrayIndex += 1
    else:
        st.markdown(f"**No split needed (base case)** {numberArray}")

#Function to print array elements in boxes
def display_array_boxes(arr, label="Array"):
    st.markdown(f"**{label}:**")
    cols = st.columns(len(arr))
    for i, num in enumerate(arr):
        cols[i].markdown(
            f"<div style='border:1px solid #888; border-radius:6px; padding:10px; text-align:center; background:#f9f9f9; font-size:15px;'>{num}</div>",
            unsafe_allow_html=True
        )

st.title("Merge Sort Algorithm")
st.text("Merge sort is a divide-and-conquer algorithm used for sorting arrays or lists. It works by repeatedly dividing the input into smaller subarrays until each subarray contains only one element, then merging these subarrays back together in sorted order (Kumar, 2022).")

#The initial unsorted array list
unsortedArray = [7, 5, 16, 24, 13, 10, 3, 20]
display_array_boxes(unsortedArray, "Sample Unsorted Array")
st.write("")
if st.button("Sort Array"):
    st.session_state.merge_count = 0  # Reset counter on each sort
    st.markdown(f"**Dividing the array**")
    mergeSort(unsortedArray)
    display_array_boxes(unsortedArray, "Final Sorted Array")
    st.markdown(f"**Total Iterations:** {st.session_state.merge_count}")

