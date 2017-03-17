% save matrix as csv file and add col headers
function dataOut(W, title)
    col_headers = zeros(size(W), 1);
    for i = 1:size(W)
        col_headers(i) = i;
    end
    
    csvwrite(title, col_headers);
    csvwrite(title, W, 1);
end
