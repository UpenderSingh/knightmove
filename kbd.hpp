char i_to_k[] ={'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', '1', '2', '3'};
bool vowels[] ={1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0};
int map[18][6] = {
    {7, 11, -1, -1, -1, -1}, 
    {8, 10, 12, -1, -1, -1}, 
    {5, 9, 11, 13, -1, -1}, 
    {6, 12, 14, -1, -1, -1}, 
    {7, 13, -1, -1, -1, -1}, 
    {2, 12, 15, -1, -1, -1}, 
    {3, 13, 16, -1, -1, -1}, 
    {0, 4, 10, 14, 15, 17}, 
    {1, 11, 16, -1, -1, -1}, 
    {2, 12, 17, -1, -1, -1}, 
    {1, 7, 16, -1, -1, -1}, 
    {0, 2, 8, 17, -1, -1}, 
    {1, 3, 5, 9, -1, -1}, 
    {2, 4, 6, 15, -1, -1}, 
    {3, 7, 16, -1, -1, -1}, 
    {5, 7, 13, -1, -1, -1}, 
    {6, 8, 10, 14, -1, -1}, 
    {7, 9, 11, -1, -1, -1}
};
