package com.example.shoponline_android.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.shoponline_android.R;
import com.example.shoponline_android.model.Product;

import java.util.List;
import java.util.Locale;

public class ProductAdapter extends RecyclerView.Adapter<ProductAdapter.ProductViewHolder> {
    public interface OnProductActionListener {
        void onEdit(Product product);

        void onDelete(Product product);
    }

    private final List<Product> products;
    private final OnProductActionListener actionListener;

    public ProductAdapter(android.content.Context context, List<Product> products, OnProductActionListener actionListener) {
        this.products = products;
        this.actionListener = actionListener;
    }

    @NonNull
    @Override
    public ProductViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.product_item, parent, false);
        return new ProductViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull ProductViewHolder holder, int position) {
        Product product = products.get(position);
        holder.tvName.setText(product.getName());
        holder.tvPrice.setText(String.format(Locale.getDefault(), "¥ %.2f", product.getPrice()));
        holder.tvCategory.setText("分类：" + product.getCategory());
        holder.tvCreatedAt.setText("创建：" + product.getCreatedAt());

        String description = product.getDescription();
        if (description == null || description.trim().isEmpty()) {
            holder.tvDescription.setText("暂无商品描述");
        } else {
            holder.tvDescription.setText(description);
        }

        if (actionListener == null) {
            holder.actionRow.setVisibility(View.GONE);
        } else {
            holder.actionRow.setVisibility(View.VISIBLE);
            holder.btnEdit.setOnClickListener(v -> actionListener.onEdit(product));
            holder.btnDelete.setOnClickListener(v -> actionListener.onDelete(product));
        }
    }

    @Override
    public int getItemCount() {
        return products.size();
    }

    static class ProductViewHolder extends RecyclerView.ViewHolder {
        TextView tvName;
        TextView tvDescription;
        TextView tvCategory;
        TextView tvPrice;
        TextView tvCreatedAt;
        LinearLayout actionRow;
        Button btnEdit;
        Button btnDelete;

        ProductViewHolder(@NonNull View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tv_product_name);
            tvDescription = itemView.findViewById(R.id.tv_product_description);
            tvCategory = itemView.findViewById(R.id.tv_product_category);
            tvPrice = itemView.findViewById(R.id.tv_product_price);
            tvCreatedAt = itemView.findViewById(R.id.tv_product_created_at);
            actionRow = itemView.findViewById(R.id.action_row);
            btnEdit = itemView.findViewById(R.id.btn_edit);
            btnDelete = itemView.findViewById(R.id.btn_delete);
        }
    }
}
