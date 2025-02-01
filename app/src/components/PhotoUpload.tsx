"use client";
import React, { useState } from "react";

const PhotoUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      // Handle the file upload logic here
      console.log("File uploaded:", selectedFile);
    }
  };

  return (
    <div className="flex flex-col items-center p-4 border border-gray-300 rounded-lg">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-4"
      />
      {preview && (
        <img
          src={preview}
          alt="Preview"
          className="w-32 h-32 object-cover mb-4"
        />
      )}
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Upload Photo
      </button>
    </div>
  );
};

export default PhotoUpload;
